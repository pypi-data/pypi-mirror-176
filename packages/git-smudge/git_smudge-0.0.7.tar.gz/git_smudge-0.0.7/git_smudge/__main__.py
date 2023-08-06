#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

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

import sys
import os
import argparse
import argcomplete
import subprocess
import logging

from git_smudge import VERSION, LANG_MAP, add_common_args
from git_smudge.config import Config, run_git

from ktpanda.cli import Parser, arg

log = logging.getLogger(__name__)

arg_parser = Parser(description=f'git_smudge version {VERSION}')
command = arg_parser.command

@command('setup',
         help="Set up the repository / worktree to enable git-smudge and create an empty "
         "configuration if it doesn't exist")
def cmd_setup(parser, args):
    cfg = load_config()
    cfg.setup()

@command('apply',
         help='Update the configuration from git-smudge.toml and apply changes to files')
@arg('-N', '--no-update-files', help="Apply the new configuration but do not update any files")
def cmd_apply(parser, args):
    cfg = load_config()
    cfg.apply(not args.no_update_files)

@command('clean',
         help='Undo any changes made to files, as if an empty configuration were applied')
def cmd_clean(parser, args):
    cfg = load_config()
    cfg.load_blank()
    cfg.apply()

@command('comment-styles',
         help='List all available values for `comment_style`')
def cmd_list_style(parser, args):
    for lang, (line, block, extensions) in LANG_MAP.items():
        extensions = ', '.join(extensions.split())
        print(f'{lang}, {extensions}:')
        if line:
            print(f'   {line[0]}LINE{line[1]}')
        if block:
            print(f'   {block[0]}BLOCK{block[1]}')
        print()

@command('edit', help='Edit the git-smudge configuration file')
@arg('-a', '--apply', action='store_true', help="Apply the new configuration after editing")
def cmd_edit(parser, args):
    cfg = load_config()
    editor = run_git(['var', 'GIT_EDITOR']).stdout.strip()
    subprocess.run(f'{editor} git-smudge.toml', shell=True, cwd=cfg.config_path.parent)
    if args.apply:
        cfg.apply()
    else:
        print('Run `git smudge apply` to apply the new configuration', file=sys.stderr)

def load_config():
    cfg = Config.from_git()
    cfg.load()
    return cfg

def add_arguments_for_main(p):
    p.set_defaults(debug=False)
    add_common_args(p)

def setup_logging(debug):
    if os.getenv('GIT_SMUDGE_DEBUG') not in {None, '', '0'}:
        debug = True

    root = logging.getLogger()
    root.setLevel(logging.DEBUG if debug else logging.INFO)

    console_formatter = logging.Formatter('git-smudge: %(levelname)s: [%(name)s] %(message)s')
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)

def main(prog='git-smudge'):
    p = arg_parser.root_parser

    add_arguments_for_main(p)

    argcomplete.autocomplete(p)

    args = p.parse_args()

    setup_logging(args.debug)

    arg_parser.dispatch(args)

if __name__ == '__main__':
    main('python3 -m git_smudge')
