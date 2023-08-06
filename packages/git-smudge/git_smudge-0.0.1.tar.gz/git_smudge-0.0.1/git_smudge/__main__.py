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

import argparse
import argcomplete

from git_smudge import VERSION, add_default_args
from git_smudge import SimpleTextFilter, InsertLineFilter, CommentOutFilter, MultiTextFilter

class AddSimpleFilterAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        namespace.filters.append(SimpleTextFilter(*values))

class AddInsertFilterAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        lines = values[1:]
        block = namespace.block if namespace.block is not None else len(lines) > 1
        namespace.filters.append(InsertLineFilter(values[0], lines, block=block))

class AddCommentFilterAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        count = None if len(values) < 2 else int(values[1])
        namespace.filters.append(CommentOutFilter(values[0], count=count))

def add_arguments_for_main(p):
    p.set_defaults(filters=[])

    add_default_args(p)

    p.add_argument(
        '-C', '--comment-style', default='auto',
        help='')

    p.add_argument(
        '--block', action='store_true',
        help='Use block mode for --insert (default: only if more than one line is inserted)')

    p.add_argument(
        '--no-block', dest='block', action='store_false',
        help='Never use block mode')

    p.add_argument(
        '--simple',
        dest='filters', action=AddSimpleFilterAction,
        nargs=2, metavar=('SEARCH', 'REPLACE'),
        help='')

    p.add_argument(
        '--insert',
        dest='filters', action=AddInsertFilterAction,
        nargs='+', metavar=('MATCH', 'LINES'),
        help='')

    p.add_argument(
        '--comment',
        dest='filters', action=AddCommentFilterAction,
        nargs='+', metavar=('MATCH', 'COUNT'),
        help='')

def main(prog='simple-git-filter'):
    p = argparse.ArgumentParser(prog=prog, description=f'git_smudge version {VERSION}')
    argcomplete.autocomplete(p)
    args = p.parse_args()

    add_arguments_for_main(p)

    argcomplete.autocomplete(p)

    args = p.parse_args()

    if len(args.filters) == 0:
        p.print_help()
        return
    elif len(args.filters) == 1:
        filter = args.filters[0]
    else:
        filter = MultiTextFilter(args.filters)

    filter.run_main(args)

if __name__ == '__main__':
    main('python3 -m git_smudge')
