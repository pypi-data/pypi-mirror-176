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
import logging

from git_smudge import VERSION, LANG_MAP, add_common_args, ConfigDispatchFilter
from git_smudge.config import Config

log = logging.getLogger(__name__)

def add_arguments_for_main(p):
    p.set_defaults(filters=[])

    add_common_args(p)

    p.add_argument(
        '--setup', action='store_true',
        help='Set up the repository to enable git-smudge and create an empty '
        'configuration if it doesn\'t exist')

    p.add_argument(
        '--list-comment-styles', action='store_true',
        help='List all available values for `comment_style`')

def setup_logging(debug):
    if os.getenv('GIT_SMUDGE_DEBUG') not in {None, '', '0'}:
        debug = True

    root = logging.getLogger()
    root.setLevel(logging.DEBUG if debug else logging.INFO)

    console_formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(console_formatter)
    root.addHandler(console_handler)

def main(prog='git-smudge'):
    p = argparse.ArgumentParser(prog=prog, description=f'git_smudge version {VERSION}')

    add_arguments_for_main(p)

    argcomplete.autocomplete(p)

    args = p.parse_args()

    setup_logging(args.debug)

    if args.setup:
        cfg = Config.from_git()
        cfg.setup()
        return

    if args.list_comment_styles:
        for lang, (line, block, extensions) in LANG_MAP.items():
            extensions = ', '.join(extensions.split())
            print(f'{lang}, {extensions}:')
            if line:
                print(f'   {line[0]}LINE{line[1]}')
            if block:
                print(f'   {block[0]}BLOCK{block[1]}')
            print()
        return

    p.print_help()

if __name__ == '__main__':
    main('python3 -m git_smudge')
