# git_smudge.config
#
# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import fnmatch
import subprocess
import logging
import tempfile

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib

from pathlib import Path

from ktpanda.fileutils import load_json, save_json

from git_smudge import GitFilter, SimpleFilter, InsertLineFilter, CommentOutFilter, FileContent

log = logging.getLogger('config')

MAX_FILTER_LIST = 5000

CONFIG_TEMPLATE = r'''
## Example configuration.
## See https://toml.io/en/v1.0.0 for TOML syntax

## List of plugins to load. The plugin can create one or more subclasses of `GitFilter`.
## Each class can be referenced by name, without `Filter` on the end.
# plugins = [
#     "plugin1.py",
#     "plugin2.py",
# ]

## Define a simple filter that applies to all .c files except foo.c
# [filters.filter1]
# type = "simple"
# search = "filter1"
# replace = "qwer"
# files = [ "*.c", "!foo.c" ]

## Define an insert filter that applies to all files in 'subdir/' except .txt files
# [filters.filter2]
# type = "InsertLine"
# after = 'filter2'
# insert = [ "test1", "test2" ]
# files = [ "subdir/*", "!*.txt" ]

## Define a multi-part filter that applies to all .js files in the project root
# [filters.filter3]
# files = "/*.js"
#
# [[filters.filter3.filters]]
# type = "InsertLine"
# after = 'old_call\(123, (.*)\)'
# insert = [ 'new_call(456, $1);']
#
# [[filters.filter3.filters]]
# type = "CommentOut"
# match = 'old_call\(123, (.*)\)'

# Add an extra match patterns
# [[rule]]
# filters = [ "filter1", "filter2" ]
# files = "!special.c"
#
# [[rule]]
# filters = "filter3"
# files  = "special.c"
'''

class CacheDict(dict):
    '''Works like `defaultdict`, except it passes the key to the factory function'''
    def __init__(self, factory):
        super().__init__()
        self.factory = factory

    def __missing__(self, key):
        r = self[key] = self.factory(key)
        return r

def run_git(cmd, check=True):
    return subprocess.run(
        ['git'] + cmd, stdout=subprocess.PIPE, check=check,
        encoding='utf8', errors='surrogateescape')

def git_path(relpath) -> Path:
    '''Return a `Path` object pointing to a file within the .git directory'''
    return Path(run_git(['rev-parse', '--git-path', relpath]).stdout.rstrip('\n'))

def _filter_list_json(lst):
    rtn = [(filt if isinstance(filt, str) else filt.config) for filt in lst]
    return rtn[0] if len(rtn) == 1 else rtn

def item_or_list(val):
    return val if isinstance(val, list) else [val]

class Pattern:
    def __init__(self, pat):
        self.dir_pattern, self.file_pattern = pat
        self.include_rules = []
        self.exclude_rules = []

class FilterConfig:
    def __init__(self, root):
        self.root = root
        self.filter_classes = {}
        self.named_filters = {}
        self.rule_patterns = {}

    @classmethod
    def load_toml(cls, tomlpath, worktree, gitdir):
        try:
            with tomlpath.open('rb') as fp:
                root = tomllib.load(fp)
        except FileNotFoundError:
            root = {}

        plugin_content = []
        new_root = {
            'plugins': plugin_content,
            'filters': root.get('filters', {}),
            'rule': root.get('rule', [])
        }

        for obj in root.get('plugins', ()):
            # support both `plugins = [ ... ]` and [[plugins]] path = ...
            if isinstance(obj, str):
                obj = { 'path': obj }
            path = obj['path']

            # If path starts with '~/', make it relative to the user's home directory. If
            # it starts with '.git/' exactly, then it's relative to the common Git directory,
            # even if it's not in the usual place.
            if path.startswith('.git/'):
                script_path = gitdir / path[5:]
            elif path.startswith('~/'):
                script_path = Path.home() / path[2:]
            else:
                script_path = worktree / path

            log.debug('Loading plugin %s', script_path)
            content = FileContent(script_path, script_path.read_bytes())
            plugin_content.append({'path': str(script_path), 'content': content.get_text().split('\n')})

        return cls(new_root)

    @classmethod
    def load_json(cls, jsonpath):
        root = load_json(jsonpath)
        if root is None:
            return cls({})

        return cls(root)

    def load(self):
        for cls in (SimpleFilter, InsertLineFilter, CommentOutFilter):
            self.add_filter_class(cls)

        for obj in self.root.get('plugins', ()):
            try:
                block = compile(
                    '\n'.join(obj['content']), obj['path'],
                    mode='exec', dont_inherit=True)

                namespace = { 'GitFilter': GitFilter }
                exec(block, namespace)

                for value in namespace.values():
                    if (isinstance(value, type)
                        and issubclass(value, GitFilter)
                        and value is not GitFilter):
                        log.debug('Adding filter class %s', value)
                        self.add_filter_class(value)
            except Exception as ex:
                raise ValueError(f'Failed to load plugin {obj["path"]} (see attached exception)') from ex

        filter_rules = CacheDict(lambda k: [])
        for rule in self.root.get('rule', ()):
            files = item_or_list(rule.get('files', []))
            for filter in item_or_list(rule.get('filters', [])):
                filter_rules[filter].extend(files)

        patterns = self.rule_patterns = CacheDict(Pattern)
        filters = self.named_filters = {}
        for name, obj in self.root.get('filters', {}).items():
            filters[name] = self.build_filter_list(obj)

            files = item_or_list(obj.get('files', []))
            files.extend(filter_rules[name])
            for pattern in files:
                if exclude := pattern.startswith('!'):
                    pattern = pattern[1:]

                # If there is no '/' in the rule, then it applies to the filename only
                dirpart, sep, filepart = pattern.rpartition('/')
                if sep:
                    dirpart = dirpart.lstrip('/')
                else:
                    dirpart = '*'

                if exclude:
                    patterns[dirpart, filepart].exclude_rules.append(name)
                else:
                    patterns[dirpart, filepart].include_rules.append(name)

        for name, filter_list in filters.items():
            self._resolve_references(filter_list)

    def add_filter_class(self, cls):
        name = cls.__name__
        if name.endswith('Filter'):
            name = name[:-6]
        #log.debug('Adding filter class %s as %s', cls, name.lower())
        self.filter_classes[name.lower()] = cls

    def get_filters_for_path(self, path):
        # Make sure path starts with exactly one slash
        dirpart, _, filepart = path.rpartition('/')

        include_rules = set()
        exclude_rules = set()
        for pat in self.rule_patterns.values():
            if (fnmatch.fnmatch(dirpart, pat.dir_pattern) and
                fnmatch.fnmatch(filepart, pat.file_pattern)):
                log.debug('%s: matches %s/%s', path, pat.dir_pattern, pat.file_pattern)
                include_rules.update(pat.include_rules)
                exclude_rules.update(pat.exclude_rules)

        include_rules -= exclude_rules
        if not include_rules:
            log.debug('%s: no filters matched', path)
            return []

        rtnlist = []
        for name, filter_list in self.named_filters.items():
            if name in include_rules:
                rtnlist.extend(filter_list)

        log.debug('Filters for %s: %r', path, rtnlist)
        return rtnlist

    def _resolve_references(self, filter_list):
        while True:
            next_filters = []
            have_references = False
            for filt in filter_list:
                if isinstance(filt, str):
                    next_filters.extend(self.named_filters[filt])
                    have_references = True
                else:
                    next_filters.append(filt)

                if len(next_filters) > MAX_FILTER_LIST:
                    raise ValueError(f'Too many filters in list ({len(next_filters)})')

            if not have_references:
                return

            filter_list[:] = next_filters

    def build_filter(self, obj):
        type = obj['type']
        cls = self.filter_classes[type.lower()]
        filter = cls(obj)
        filter.update_config()
        return filter

    def _build_filter_list(self, filter_list, obj):
        if isinstance(obj, dict):
            sub_filters = obj.get('filters')
            if sub_filters:
                self._build_filter_list(filter_list, sub_filters)

            if obj.get('type'):
                filter_list.append(self.build_filter(obj))

        elif isinstance(obj, list):
            for part in obj:
                self._build_filter_list(filter_list, part)

        elif isinstance(obj, str):
            filter_list.append(obj)
        else:
            raise TypeError(f'Invalid value in filter list: {obj!r}')

    def build_filter_list(self, obj):
        filter_list = []
        self._build_filter_list(filter_list, obj)
        return filter_list

class Config:
    def __init__(self, worktree, git_dir, git_common_dir=None, config_path=None):
        self.worktree = worktree
        self.git_dir = git_dir
        self.git_common_dir = git_common_dir or git_dir

        self.working_config = None
        self.new_config = None

        if config_path is None:
            config_path = git_dir / f'git-smudge.toml'
        self.config_path = config_path
        self.working_config_path = config_path.with_name(f'worktree-git-smudge.json')

    @classmethod
    def from_git(cls):
        paths = run_git([
            'rev-parse', '--show-toplevel', '--git-dir',
            '--git-common-dir', '--git-path', 'git-smudge.toml'
        ]).stdout.replace('\r\n', '\n').rstrip('\n').split('\n')

        worktree, gitdir, gitcommon, configpath = paths

        return cls(Path(worktree), Path(gitdir), Path(gitcommon), Path(configpath))

    def check_config_newer(self):
        '''Check if the user configuration has been changed since the last time
        `git smudge apply` was run'''
        try:
            wt_mtime = self.working_config_path.stat().st_mtime
        except FileNotFoundError:
            wt_mtime = 0

        try:
            config_mtime = self.config_path.stat().st_mtime
            if config_mtime > wt_mtime:
                return True
        except FileNotFoundError:
            pass

        return False

    def warn_config_newer(self):
        if self.check_config_newer():
            log.warn('Configuration %s has changed, please run `git smudge apply`',
                     self.config_path)

    def load(self):
        self.working_config = FilterConfig.load_json(self.working_config_path)
        self.working_config.load()

    def save_json(self, root):
        new_root = {
            'note': [
                "DO NOT EDIT THIS FILE. EDIT git-smudge.toml, THEN RUN",
                "`git smudge apply` TO APPLY CONFIGURATION CHANGES"
            ],
            'plugins': root.get('plugins', []),
            'filters': root.get('filters', {}),
            'rule': root.get('rule', [])
        }
        save_json(self.working_config_path, new_root)

    def load_new(self):
        self.new_config = FilterConfig.load_toml(
            self.config_path, self.worktree, self.git_common_dir)
        self.new_config.load()

    def load_blank(self):
        self.new_config = FilterConfig({})
        self.new_config.load()



    def apply(self, update_files=True):
        if not self.new_config:
            self.load_new()

        if not update_files:
            self.save_json(self.new_config.root)
            return

        # Get a list of all files tracked in the repository. `git ls-files -z` will spit
        # out a NUL-separated list.
        repo_files = run_git(['ls-files', '-z']).stdout.split('\0')

        # If there are no files, or there was a terminating NUL, there will be a blank
        # item at the end
        if repo_files[-1] == '':
            repo_files.pop()

        change_count = 0
        written_files = []
        try:
            for path in repo_files:
                # Run the file through the `clean` method of the old filters, then the
                # `smudge` method of the new filters.
                old_filters = self.working_config.get_filters_for_path(path)
                new_filters = self.new_config.get_filters_for_path(path)
                if old_filters or new_filters:
                    fpath = self.worktree / path

                    prev_data = fpath.read_bytes()
                    content = FileContent(fpath, prev_data, True)

                    for filter in reversed(old_filters):
                        filter.clean(content)

                    content.is_smudged = False

                    for filter in new_filters:
                        filter.smudge(content)

                    if content.changed:
                        new_data = content.get_binary()
                        if new_data != prev_data:
                            change_count += 1
                            log.info('apply: Content of %s has changed', path)
                            tf = tempfile.NamedTemporaryFile(
                                dir=str(fpath.parent), prefix=fpath.name,
                                suffix='.smudge-apply-temp', delete=False, mode='wb')
                            written_files.append((fpath, tf.name))
                            with tf:
                                tf.write(new_data)

                            try:
                                os.chmod(tf.name, fpath.stat().st_mode)
                            except OSError as e:
                                # Don't get too worked up about a chmod failure
                                log.debug('Failed to chmod %s: %s', tf.name, e)

            # Save the new config.
            self.save_json(self.new_config.root)

            # Now we're ready to commit all the files. There's no going back now.
            to_replace = written_files

            # Clear this out - if we fail to replace the files with the temporaries, just
            # leave the temporaries for the user to sort out.
            written_files = []

            for path, temppath in to_replace:
                try:
                    os.replace(temppath, path)
                except OSError as e:
                    log.error('Could not apply new content to %s: %s', path, e)
                    log.error('Keeping temporary file %s.', temppath)

            log.info('git-smudge configuration updated for %s, %d files changed',
                     self.worktree, change_count)

        finally:
            for path, temppath in written_files:
                try:
                    os.unlink(temppath)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    log.warn('Failed to remove temporary path %s: %s', temppath, e)

    def setup(self):
        '''Prepare a git repository. Set up `git config` to define our filter, add an
        entry to `.git/info/attributes, and create an empty '''
        if not self.config_path.exists():
            self.config_path.write_text(CONFIG_TEMPLATE, encoding='ascii')
            print(f'Created template configuration in {self.config_path.absolute()}')
        else:
            print(f'Configuration {self.config_path.absolute()} already exists')

        exe_esc = sys.executable.replace("'", r"'\''")
        cmd = f"'{exe_esc}' -m git_smudge.runfilter"
        run_git(['config', 'filter.git-smudge.process', cmd])

        attributes = git_path('info/attributes')
        try:
            attribute_data = attributes.read_bytes()
        except FileNotFoundError:
            attribute_data = b''

        content = FileContent(attributes, attribute_data)
        text = content.get_text()

        insert = '* filter=git-smudge'
        if insert not in text:
            if text and not text.endswith('\n'):
                text += '\n'

            text += (
                f'# Added by `git-smudge setup`\n'
                f'{insert}\n'
            )
            content.set_text(text)
            attributes.write_bytes(content.get_binary())
            print(f'Inserted {insert!r} into {attributes}')
        print(f'Repository {self.worktree.absolute()} set up for git-smudge')
