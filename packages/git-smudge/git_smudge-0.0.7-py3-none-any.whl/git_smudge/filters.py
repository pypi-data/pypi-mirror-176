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

import re
import logging

from git_smudge import GitFilter, get_comment_style

RX_SPACE = re.compile(r'[ \t]*')

log = logging.getLogger('filters')

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

class SimpleFilter(GitFilter):
    def _set_from_config(self, /, search, replace, check=True, **kw):
        super()._set_from_config(**kw)
        self.search = search
        self.replace = replace
        self.check = check

    def clean(self, content):
        if content.is_smudged:
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

        if isinstance(insert, str):
            insert = insert.split('\n')
            if insert[-1] == '':
                insert.pop()

        self.lines = insert

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
