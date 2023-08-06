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

from git_smudge import VERSION, LANG_MAP, add_default_args
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
        namespace.filters.append(CommentOutFilter(values[0]))

class SetFilterAction(argparse.Action):
    use_const = False
    def __call__(self, parser, namespace, value, option_string=None):
        if not namespace.filters:
            raise ValueError(f'{option_string} must be specified after a filter')

        if not hasattr(namespace.filters[-1], self.dest):
            raise ValueError(f'{option_string} does not apply to last specified filter')

        setattr(namespace.filters[-1], self.dest, self.const if self.use_const else value)

class SetFilterConstAction(SetFilterAction):
    use_const = True

def add_arguments_for_main(p):
    p.set_defaults(filters=[])

    add_default_args(p)

    p.add_argument(
        '-C', '--comment-style', default='auto',
        help='Comment style (e.g. py, xml). Default: auto, which tries to determine '
        'the comment style based on the filename extension. Use `-C list` to list '
        'available languages and associated extensions.')


    g = p.add_argument_group('Simple filter')

    g.add_argument(
        '--simple',
        dest='filters', action=AddSimpleFilterAction,
        nargs=2, metavar=('SEARCH', 'REPLACE'),
        help='Add a simple, exact replacement filter.')

    g = p.add_argument_group('Line insert filter')

    g.add_argument(
        '--insert',
        dest='filters', action=AddInsertFilterAction,
        nargs='+', metavar=('MATCH', 'LINES'),
        help='Insert code lines into a file. `MATCH` is a regular expression which '
        'should match a line of code, after which `LINES` will be inserted.')

    g.add_argument(
        '--block', action=SetFilterConstAction, dest='block', nargs=0, const=True,
        help='Force block mode for the last --insert filter (surround inserted lines '
        'with begin/end marker comments) Default: only if more than one line is inserted')

    g.add_argument(
        '--line', action=SetFilterConstAction, dest='block', nargs=0, const=False,
        help='Force line mode for the last --insert filter (put a marker comment at the '
        'end of each inserted line)')


    g = p.add_argument_group('Comment-out filter')

    g.add_argument(
        '--comment',
        dest='filters', action=AddCommentFilterAction,
        nargs=1, metavar='MATCH',
        help='Comment out lines of code in a file.')

    g.add_argument(
        '--count', action=SetFilterAction, dest='count', type=int,
        help='Set a maximum match count for the last --comment filter. Default: comment '
        'out all matching lines')


def main(prog='git-smudge'):
    p = argparse.ArgumentParser(prog=prog, description=f'git_smudge version {VERSION}')

    add_arguments_for_main(p)

    argcomplete.autocomplete(p)

    args = p.parse_args()
    if args.comment_style == 'list':
        for lang, (line, block, extensions) in LANG_MAP.items():
            extensions = ', '.join(extensions.split())
            print(f'{lang}, {extensions}:')
            if line:
                print(f'   {line[0]}LINE{line[1]}')
            if block:
                print(f'   {block[0]}BLOCK{block[1]}')
            print()
        return

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
