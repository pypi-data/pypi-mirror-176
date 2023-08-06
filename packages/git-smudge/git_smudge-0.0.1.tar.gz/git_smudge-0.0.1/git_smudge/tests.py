#!/usr/bin/python3
import argparse
import unittest
from pathlib import Path

import git_smudge
import git_smudge.__main__


def build_clean_text(pre_text, indent, match_part, post_text, **kw):
    return pre_text + indent + match_part + post_text

def build_insert_test_smudge_block(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}{indent}{match_part}'
        f'\n{indent}{comment[0]}BEGIN SMUDGE InsertLineFilter{comment[1]}'
        + ''.join(f'\n{indent}{line}' for line in lines) +
        f'\n{indent}{comment[0]}END SMUDGE InsertLineFilter{comment[1]}'
        f'{post_text}'
    )
def build_insert_test_smudge_line(pre_text, indent, match_part, post_text, lines, comment, **kw):
    return (
        f'{pre_text}{indent}{match_part}'
        + ''.join(f'\n{indent}{line} {comment[0]}LINE SMUDGE InsertLineFilter{comment[1]}' for line in lines) +
        f'{post_text}'
    )

def build_comment_out_text(pre_text, indent, match_part, post_text, comment, **kw):
    text = []
    for line in (indent + match_part).split('\n'):
        split_pos = len(indent) if line.startswith(indent) else 0
        text.append(f'{line[:split_pos]}{comment[0]}SMUDGE CommentOutFilter [{line[split_pos:]}]{comment[1]}')
    return pre_text + '\n'.join(text) + post_text


TEST_LINES = [
    'insert test line 1',
    '    insert test with leading space',
    'insert test with trailing space ',
]

INSERT_TESTS = []

MATCH_PARTS = [
    ('im_start im_end'),
    ('pre im_start im_end'),
    ('im_start im_end post'),
    ('pre im_start im_end post'),
    ('ml im_start(\n\ttest\n  )im_end post'),
]

for pre_text in ('', 'pre_text\n'):
    for post_text in ('', '\n', '\nextra_text'):
        for indent in ('', '   ', '\t', '\t '):
            for match_part in MATCH_PARTS:
                INSERT_TESTS.append({
                    'pre_text': pre_text,
                    'indent': indent,
                    'match_part': match_part,
                    'post_text': post_text,
                })


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def do_test_filter(self, filter, kw, path, expect):
        clean = build_clean_text(**kw)
        with self.subTest(t=clean, s=expect, p=path, **kw):
            smudge_output = filter.smudge_text(clean, path, False, False)
            self.assertEqual(smudge_output, expect)

            cleaned = filter.clean_text(expect, path, False, False, False)

            # First make sure that it actually changed the text
            self.assertNotEqual(cleaned, expect)

            self.assertEqual(cleaned, clean)

    def do_test_inserts(self, comment_style, path, comments, block):
        filter = git_smudge.InsertLineFilter(
            '(?s)im_start.*im_end', TEST_LINES, comment_style=comment_style,
            block=block
        )
        f = build_insert_test_smudge_block if block else build_insert_test_smudge_line
        for kw in INSERT_TESTS:
            smudge_expect = f(**kw, lines=TEST_LINES, comment=comments)
            self.do_test_filter(filter, kw, path, smudge_expect)


    def test_insert_block_c(self):
        self.do_test_inserts('c', Path('test.xxx'), git_smudge.COMMENT_C, True)

    def test_insert_block_sql(self):
        self.do_test_inserts('auto', Path('test.sql'), git_smudge.COMMENT_SQL, True)

    def test_insert_line_xml(self):
        self.do_test_inserts('auto', Path('test.xml'), git_smudge.COMMENT_XML, True)

    def test_insert_line_cpp(self):
        self.do_test_inserts('auto', Path('test.cpp'), git_smudge.COMMENT_CPP, True)

    def test_comment_out(self):
        filter = git_smudge.CommentOutFilter(
            '(?s)im_start.*im_end', comment_style='auto',
        )
        comment_styles = [
            ('test.py', git_smudge.COMMENT_HASH),
            ('test.xml', git_smudge.COMMENT_XML),
            ('test.c', git_smudge.COMMENT_C),
        ]
        for i, kw in enumerate(INSERT_TESTS):
            fname, comments = comment_styles[i % len(comment_styles)]
            commented = build_comment_out_text(comment=comments, **kw)
            self.do_test_filter(filter, kw, Path(fname), commented)

    def get_filters_for_args(self, argv):
        p = argparse.ArgumentParser(description='')
        git_smudge.__main__.add_arguments_for_main(p)
        args = p.parse_args(argv)
        return args.filters

    def test_args_1(self):
        filters = self.get_filters_for_args(
            ['--simple', 'abcd', 'defg']
        )

        self.assertEqual(len(filters), 1)
        self.assertIsInstance(filters[0], git_smudge.SimpleTextFilter)
        self.assertEqual(filters[0].search, 'abcd')
        self.assertEqual(filters[0].replace, 'defg')

    def test_args_2(self):
        filters = self.get_filters_for_args([
            '--insert', 'match_text_1', 'insert 1',
            '--insert', 'match_text_2', 'insert 1', 'insert 2',
            '--simple', 'abcd', 'defg'
        ])

        self.assertEqual(len(filters), 3)

        self.assertIsInstance(filters[0], git_smudge.InsertLineFilter)
        self.assertEqual(filters[0].insert_after.pattern, 'match_text_1')
        self.assertListEqual(filters[0].lines, ['insert 1'])
        self.assertEqual(filters[0].block, False)

        self.assertIsInstance(filters[1], git_smudge.InsertLineFilter)
        self.assertEqual(filters[1].insert_after.pattern, 'match_text_2')
        self.assertListEqual(filters[1].lines, ['insert 1', 'insert 2'])
        self.assertEqual(filters[1].block, False)

        self.assertIsInstance(filters[2], git_smudge.SimpleTextFilter)
        self.assertEqual(filters[2].search, 'abcd')
        self.assertEqual(filters[2].replace, 'defg')

    def test_args_3(self):
        filters = self.get_filters_for_args([
            '--block',
            '--insert', 'match_text_1', 'insert 1',
            '--no-block',
            '--insert', 'match_text_2', 'insert 1', 'insert 2',
        ])

        self.assertEqual(len(filters), 2)
        self.assertEqual(filters[0].block, True)
        self.assertEqual(filters[1].block, False)

if __name__ == '__main__':
    unittest.main()
