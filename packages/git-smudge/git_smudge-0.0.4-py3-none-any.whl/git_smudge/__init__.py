# git_smudge
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

'''
git_smudge
==========

A filter driver for Git which cam make local changes to a repository.
'''

import sys
import re
import time
import os
import argparse
import subprocess
import traceback
import struct
import logging
from io import BytesIO
from pathlib import Path

import argcomplete

proc_log = logging.getLogger('git-process')
filt_log = logging.getLogger('filters')

VERSION = "0.0.4"

RX_SPACE = re.compile(r'[ \t]*')

MAX_PACKET_CONTENT_SIZE = 65516
BOM = '\ufeff'
DEBUG = False

# Line comments
COMMENT_HASH = '# ', ''
COMMENT_DSLASH = '// ', ''
COMMENT_SEMI = '; ', ''
COMMENT_DDASH = '-- ', ''
COMMENT_EXCL = '! ', ''
COMMENT_PCT = '% ', ''
COMMENT_REM = 'REM ', ''
COMMENT_QUOT = "' ", ''

# Block comments
COMMENT_C = '/* ', ' */'
COMMENT_PS = '<* ', ' *>'
COMMENT_SGML = '<!-- ', ' -->'
COMMENT_PASCAL = '(* ', ' *)'
COMMENT_HASKELL = '{- ', ' -}'
COMMENT_LUA = '--[=[ ', ' ]=]'

EXT_MAP = {}
LANG_MAP = {}

# This is by no means a comprehensive list. I went through this page:
# https://en.wikipedia.org/wiki/Comparison_of_programming_languages_(syntax)#Comments
# and just added a bunch of them
LANG_MAP = {
    # Shell-like
    'Python':     (COMMENT_HASH,   None,            'py'),
    'Shell':      (COMMENT_HASH,   None,            'sh bash'),
    'Ruby':       (COMMENT_HASH,   None,            'rb'),
    'Perl':       (COMMENT_HASH,   None,            'pl pm'),
    'Raku':       (COMMENT_HASH,   None,            'raku rakumod rakudoc rakutest t'),
    'Elixir':     (COMMENT_HASH,   None,            'ex exs'),
    'Julia':      (COMMENT_HASH,   None,            'jl'),
    'Config':     (COMMENT_HASH,   None,            'conf ini'),
    'Nim':        (COMMENT_HASH,   None,            'nim nims nimble'),

    # C-like
    'C':          (COMMENT_DSLASH, COMMENT_C,       'c h'),
    'C++':        (COMMENT_DSLASH, COMMENT_C,       'cpp hpp c++ h++ cc hh'),
    'Rust':       (COMMENT_DSLASH, None,            'rs rlib'),
    'CSS':        (None,           COMMENT_C,       'css'),
    'Java':       (COMMENT_DSLASH, COMMENT_C,       'java'),
    'Javascript': (COMMENT_DSLASH, COMMENT_C,       'js ts'),
    'Swift':      (COMMENT_DSLASH, COMMENT_C,       'swift'),
    'PHP':        (COMMENT_DSLASH, COMMENT_C,       'php'),

    # SGML
    'HTML':       (None,           COMMENT_SGML,    'html'),
    'XML':        (None,           COMMENT_SGML,    'xml'),
    'SGML':       (None,           COMMENT_SGML,    'html xml sgml'),

    # ';'
    'Lisp':       (COMMENT_SEMI,   None,            'el scm'),
    'Assembler':  (COMMENT_SEMI,   None,            'asm s'),
    'Autohotkey': (COMMENT_SEMI,   None,            'ahk'),

    # '--'
    # Some SQL variants support /* */, but not all
    'SQL':        (COMMENT_DDASH,  None,            'sql'),
    'Lua':        (COMMENT_DDASH,  COMMENT_LUA,     'lua'),
    'Ada':        (COMMENT_DDASH,  None,            'ada'),
    'Haskell':    (COMMENT_DDASH,  COMMENT_HASKELL, 'hs lhs'),
    'Eiffel':     (COMMENT_DDASH,  None,            'e'),

    # '%'
    'MATLAB':     (COMMENT_PCT,    None,            'm p mex mat fig mlx mlapp'),
    'Erlang':     (COMMENT_PCT,    None,            'erl hrl'),
    'TeX':        (COMMENT_PCT,    None,            'tex'),
    'Postscript': (COMMENT_PCT,    None,            'ps'),

     # Weirdos
    'Fortran 90': (COMMENT_EXCL,   None,            'f for f90'),
    'Pascal':     (None,           COMMENT_PASCAL,  'pas'),
    'Batch':      (COMMENT_REM,    None,            'bat'),
    'Visual Basic':(COMMENT_QUOT,  None,            'vb vba vbs bas'),
}

def _fill_comment_map():
    for item in LANG_MAP.items():
        EXT_MAP[item[0].lower()] = item
        for extn in item[1][2].split():
            EXT_MAP[extn] = item

def get_comment_style(ext, path=None, prefer_block=False):
    if not EXT_MAP:
        _fill_comment_map()

    if ext == 'auto' and path:
        ext = path.suffix.strip('.')

    ext = ext.lower()

    defn = EXT_MAP.get(ext)
    if defn is None:
        defn = 'Unknown', (COMMENT_HASH, None, ext)

    line_comment, block_comment, _ = defn[1]
    if line_comment is None:
        return block_comment

    if block_comment is None:
        return line_comment

    return block_comment if prefer_block else line_comment

def line_begin(text, pos):
    '''Find the beginning of the line containing `pos` (which may be on the newline at the
    end of the line)'''
    try:
        return text.rindex('\n', 0, pos) + 1
    except ValueError:
        return 0

def line_end(text, pos):
    '''Find the end of the line containing `pos`'''
    try:
        return text.index('\n', pos)
    except ValueError:
        return len(text)

def add_single_run_args(p):
    '''Add the common arguments to an `argparse.ArgumentParser`'''
    p.add_argument(
        '-s', '--smudge',
        dest='clean', action='store_false', default=None,
        help='Filter data from STDIN and apply working tree changes')

    p.add_argument(
        '-c', '--clean',
        dest='clean', action='store_true',
        help='Filter data from STDIN and undo working tree changes')

    p.add_argument(
        '-p', '--path', type=Path,
        help='Path to the file being processed')

    p.add_argument(
        '-P', '--process', action='store_true',
        help='Run the filter in "process" mode, filtering multiple files')

def add_common_args(p):
    '''Add common arguments to an `argparse.ArgumentParser`'''
    p.add_argument(
        '-D', '--debug', action='store_true',
        help='Show debugging output. Always set true if environment variable '
        'GIT_SMUDGE_DEBUG is set to "1"')

class FileContent:
    '''Represents the contents of a file being processed. Contains information on how to
    re-encode the contents back to binary.'''

    def __init__(self, path, data, is_smudged=False):
        self.path = path
        self.text_data = None
        self.bin_data = data
        self.encoding = 'utf8'
        self.has_bom = False
        self.is_dos = False
        self.is_smudged = False
        self.changed = False

    def get_text(self):
        '''Retrieves the current text, converting it from binary if necessary'''
        if self.text_data is not None:
            return self.text_data

        data = self.bin_data

        if data.startswith(b'\xff\xfe'):
            fmt = 'utf-16le'
        elif data.startswith(b'\xfe\xff'):
            fmt = 'utf-16be'
        else:
            fmt = 'utf8'

        try:
            text = data.decode(fmt)
        except UnicodeDecodeError:
            fmt = 'utf8'
            text = data.decode(fmt, 'surrogateescape')

        self.encoding = fmt

        self.has_bom = text.startswith(BOM)
        if self.has_bom:
            text = text[1:]

        self.is_dos = '\r\n' in text
        if self.is_dos:
            text = text.replace('\r\n', '\n')

        self.text_data = text
        return text

    def get_binary(self):
        '''Retrieves the current binary data, converting it from text if necessary.'''
        if self.bin_data is not None:
            return self.bin_data

        text = self.text_data

        if self.is_dos:
            text = text.replace('\n', '\r\n')

        if self.has_bom:
            text = BOM + text

        errors = 'surrogateescape' if self.encoding == 'utf8' else None
        data = self.bin_data = text.encode(self.encoding, errors)
        return data

    def set_text(self, text):
        '''Set the text content and clear cached binary content.'''
        self.text_data = text
        self.bin_data = None
        self.changed = True

    def set_binary(self, data):
        '''Set the binary content and clear cached text content.'''
        self.bin_data = data
        self.text_data = None
        self.changed = True

class GitFilter:
    args = None

    def __init__(self, config=None, **kw):
        if config is None:
            config = {}
        self.config = config
        if kw:
            config.update(kw)

    def _set_from_config(self, **kw):
        pass

    def update_config(self):
        self._set_from_config(**self.config)

    def read_packet(self):
        length_data = sys.stdin.buffer.read(4)
        if not length_data:
            raise EOFError()


        proc_log.debug('length = %r', length_data)

        ln = int(length_data.decode('ascii'), 16)
        if ln == 0:
            pkt = None
        else:
            pkt = sys.stdin.buffer.read(ln - 4)

        proc_log.debug('read packet %d %r', ln, pkt)

        return pkt

    def read_packet_text(self):
        data = self.read_packet()
        return None if data is None else data.decode('utf8').rstrip('\n')

    def write_packet(self, val):
        if isinstance(val, str):
            val = (val + '\n').encode('utf8')
        length_data = f'{len(val) + 4:04X}'.encode('ascii')

        proc_log.debug('write packet %r %r', length_data, val)
        sys.stdout.buffer.write(length_data)
        sys.stdout.buffer.write(val)

    def flush(self):
        proc_log.debug('flush')

        sys.stdout.buffer.write(b'0000')
        sys.stdout.buffer.flush()

    def expect_packet(self, expect):
        pkt = self.read_packet_text()
        if pkt != expect:
            raise ValueError(f'Expected {expect!r}, got {pkt!r}')

    def get_filters(self, path):
        return (self,)

    def clean(self, content):
        pass

    def smudge(self, content):
        pass

    def read_key_val(self):
        rtn = {}
        while True:
            pkt = self.read_packet_text()
            if pkt is None:
                return rtn
            key, _, val = pkt.partition('=')
            if key in rtn:
                rtn[key] = rtn[key] + '\n' + val
            else:
                rtn[key] = val

    def run_process(self):
        try:
            # Make sure stdout is in binary mode on Windows. Use `getattr` so pylint
            # doesn't complain about the attribute being missing.
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), getattr(os, 'O_BINARY'))
        except (ImportError, AttributeError):
            pass

        ident = self.read_packet_text()
        if ident != 'git-filter-client':
            raise ValueError(f'Invalid ident {ident!r}')

        header = self.read_key_val()
        if header.get('version') != '2':
            raise ValueError(f'Invalid version {header.get("version")}')

        self.write_packet('git-filter-server')
        self.write_packet('version=2')
        self.flush()

        caps = self.read_key_val()

        self.write_packet('capability=clean')
        self.write_packet('capability=smudge')
        self.flush()

        while True:
            header = self.read_key_val()
            cmd = header['command']
            path = header['pathname']

            if not path:
                raise ValueError('Empty path')

            filters = self.get_filters(path)
            if not filters:
                proc_log.debug('No filters for %s, bailing early', path)
                # Read the data and discard it
                while self.read_packet() is not None:
                    pass
                self.write_packet('status=error')
                self.flush()
                continue

            fp = BytesIO()
            while True:
                pkt = self.read_packet()
                if not pkt:
                    break
                fp.write(pkt)

            data = fp.getvalue()
            if cmd in {'clean', 'smudge'}:
                content = FileContent(Path(path), data, cmd == 'clean')

                try:
                    for cf in reversed(filters):
                        cf.clean(content)
                    self.clean(content)
                    if cmd == 'smudge':
                        for cf in filters:
                            cf.smudge(content)

                except Exception:
                    traceback.print_exc()
                    self.write_packet('status=error')
                    self.flush()
                    continue
            else:
                raise ValueError('Invalid command: {command!r}')

            if not content.changed:
                proc_log.debug('Filters for %s did not change content', path)
                self.write_packet('status=error')
                self.flush()
                continue

            self.write_packet('status=success')
            self.flush()

            fp = BytesIO(content.get_binary())
            while True:
                pkt = fp.read(MAX_PACKET_CONTENT_SIZE)
                if not pkt:
                    break
                self.write_packet(pkt)
            self.flush()
            self.flush()

    def filter_one(self, path, clean):
        data = sys.stdin.buffer.read()
        content = FileContent(path, data, clean)
        try:
            self.clean(content)
            if not clean:
                self.smudge(content)
        except Exception:
            sys.stdout.buffer.write(data)
            traceback.print_exc()
        else:
            sys.stdout.buffer.write(content.get_binary())

    def add_extra_arguments(self, p):
        pass

    def run_main_other(self):
        print('Must specify --smudge, --clean, or --process')

    def run_main(self):
        '''Run this filter in standalone mode'''
        self.update_config()

        p = argparse.ArgumentParser(description='')
        add_common_args(p)
        add_single_run_args(p)
        self.add_extra_arguments(p)
        argcomplete.autocomplete(p)
        args = p.parse_args()

        self.args = args
        if args.process:
            try:
                self.run_process()
            except EOFError:
                pass
        elif args.clean is not None:
            self.filter_one(args.path, args.clean)
        else:
            self.run_main_other()

    def __repr__(self):
        params = ", ".join(f'{k}={v!r}' for k, v in self.config.items())
        return f'{type(self).__name__}({params})'

class MultiFilter(GitFilter):
    def __init__(self, filters):
        super().__init__({})
        self.filters = filters

    def update_config(self):
        for cf in self.filters:
            cf.update_config()

    def get_filters(self, path):
        return self.filters

class ConfigDispatchFilter(GitFilter):
    def __init__(self, config):
        super().__init__()
        self.cfg = config

    def get_filters(self, path):
        return self.cfg.get_filters_for_path(path)

class SimpleFilter(GitFilter):
    def _set_from_config(self, /, search, replace, idempotent=True, **kw):
        super()._set_from_config(**kw)
        self.search = search
        self.replace = replace
        self.idempotent = idempotent

    def clean(self, content):
        if content.is_smudged or self.idempotent:
            content.set_text(content.get_text().replace(self.replace, self.search))

    def smudge(self, content):
        content.set_text(content.get_text().replace(self.search, self.replace))

class InsertLineFilter(GitFilter):
    '''Inserts one or more lines of code after a matching line of code. `insert_after` is
    a regular expression, which should match some text in the file. `lines` will be
    inserted'''

    def _set_from_config(self, /, after, insert, marker_text='SMUDGE InsertLineFilter',
                        comment_style='auto', block=None, **kw):

        super()._set_from_config(**kw)

        self.lines = insert.split('\n')
        if self.lines[-1] == '':
            self.lines.pop()

        self.comment_style = comment_style
        self.block = block if block is not None else len(self.lines) > 1
        self.marker_text = marker_text
        self.marker_esc = re.escape(marker_text)

        if isinstance(after, str):
            after = re.compile(after)

        self.insert_after = after

    def clean(self, content):
        comment_b, comment_e = map(re.escape, get_comment_style(self.comment_style, content.path))
        if self.block:
            remove_rx = (
                r'(?s)\n[\ \t]*'
                f'{comment_b}BEGIN {self.marker_esc}{comment_e}'
                r'.*?'
                f'{comment_b}END {self.marker_esc}{comment_e}'
                r'((?=\n)|$)')
        else:
            remove_rx = fr'(?s)\n[^\n]*{comment_b}LINE {self.marker_esc}{comment_e}((?=\n)|$)'
        content.set_text(re.sub(remove_rx, '', content.get_text()))

    def smudge(self, content):
        text = content.get_text()
        m = self.insert_after.search(text)
        if not m:
            return

        comment_b, comment_e = get_comment_style(self.comment_style, content.path)

        # Find the end of the line where insert_after matched.
        insert_point = line_end(text, m.end())
        prev_line_begin = line_begin(text, m.start())

        pre_text = text[:insert_point]
        post_text = text[insert_point:]

        # Get the indentation of the first matching line
        indent = RX_SPACE.match(text, prev_line_begin).group(0)

        new_text = [pre_text]
        if self.block:
            new_text.append(f'\n{indent}{comment_b}BEGIN {self.marker_text}{comment_e}')
            for line in self.lines:
                new_text.append(f'\n{indent}{line}')
            new_text.append(f'\n{indent}{comment_b}END {self.marker_text}{comment_e}')
        else:
            for line in self.lines:
                new_text.append(f'\n{indent}{line} {comment_b}LINE {self.marker_text}{comment_e}')

        new_text.append(post_text)
        content.set_text(''.join(new_text))

class CommentOutFilter(GitFilter):
    def _set_from_config(self, /, match, marker_text='SMUDGE CommentOutFilter',
                        comment_style='auto', count=None, **kw):
        super()._set_from_config(**kw)
        self.marker_text = marker_text
        self.marker_esc = re.escape(marker_text)
        self.count = count
        self.comment_style = comment_style

        if isinstance(match, str):
            match = re.compile(match, re.S)

        self.match = match

    def clean(self, content):
        comment_b, comment_e = map(re.escape, get_comment_style(self.comment_style, content.path))
        content.set_text(
            re.sub(
                fr'(?s){comment_b}{self.marker_esc} \[([^\n]*)\]{comment_e}',
                r'\1',
                content.get_text()
            )
        )

    def smudge(self, content):
        comment_b, comment_e = get_comment_style(self.comment_style, content.path)

        comment_begin = f'{comment_b}{self.marker_text} ['
        comment_end = f']{comment_e}'
        out_text = []
        remaining_text = content.get_text()
        count = self.count
        while True:
            if count is not None:
                if count == 0:
                    break
                count -= 1

            m = self.match.search(remaining_text)
            if not m:
                break

            split_a = line_begin(remaining_text, m.start())
            split_b = line_end(remaining_text, m.end())
            out_text.append(remaining_text[:split_a])
            comment_lines = remaining_text[split_a : split_b]
            remaining_text = remaining_text[split_b:]

            indent = RX_SPACE.match(comment_lines).group(0)
            for line in comment_lines.split('\n'):
                split_pos = len(indent) if line.startswith(indent) else 0
                out_text.append(
                    f'{line[:split_pos]}{comment_begin}{line[split_pos:]}{comment_end}'
                )
                out_text.append('\n')
            out_text.pop()

        out_text.append(remaining_text)
        content.set_text(''.join(out_text))
