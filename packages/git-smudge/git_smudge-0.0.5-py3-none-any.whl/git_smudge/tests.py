#!/usr/bin/python3
import argparse
import unittest
import tempfile
import shutil
import logging
from pathlib import Path

import git_smudge
import git_smudge.__main__
from git_smudge import config

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

CONFIG_TEST_PATHS = [
    ('root.txt', []),
    ('root.c', [
        ('SimpleFilter', 'search', 'filter1')
    ]),
    ('foo.c', [
        ('TestFilter', 'test', '1234')
    ]),
    ('root.py', [
        ('SimpleFilter', 'search', 'root')
    ]),
    ('subdir/test.c', [
        ('SimpleFilter', 'search', 'filter1'),
        ('CommentOutFilter', 'match', 'filter3'),
        ('SimpleFilter', 'search', 'filter1'),
        ('InsertLineFilter', 'after', 'filter2')
    ]),
    ('subdir/foo.c', [
        ('CommentOutFilter', 'match', 'filter3'),
        ('SimpleFilter', 'search', 'filter1'),
        ('InsertLineFilter', 'after', 'filter2'),
        ('TestFilter', 'test', '1234')
    ]),
    ('subdir/foo.txt', []),
    ('subdir/notroot.py', [
        ('CommentOutFilter', 'match', 'filter3'),
        ('SimpleFilter', 'search', 'filter1'),
        ('InsertLineFilter', 'after', 'filter2')
    ]),
    ('subdir/special.c', [
        ('CommentOutFilter', 'match', 'filter3'),
        ('SimpleFilter', 'search', 'filter1'),
    ]),
    ('subdir2/special.c', [
        ('CommentOutFilter', 'match', 'filter3'),
        ('SimpleFilter', 'search', 'filter1'),
    ]),
]

CONFIG_TOML = '''
plugins = [
    "plugin-test.py"
]

[filters.filter1]
type = "simple"
search = "filter1"
replace = "qwer"
files = ["*.c", "!foo.c" ]

[filters.filter2]
filters = "filter3"
type = "InsertLine"
after = 'filter2'
insert = [ "test1", "test2" ]
files = [ "subdir/*", "!*.txt" ]

[filters.filter3]
filters = [
   { type = 'CommentOut', match = 'filter3' },
   "filter1"
]

[[rule]]
filters = [ "filter1", "filter2" ]
files = "!special.c"

[[rule]]
filters = "filter3"
files  = "special.c"

[filters.foo]
type = "test"
test = "1234"
files = "foo.c"

[filters.rootpy]
type = "Simple"
search = "root"
replace = "boot"
files = "/*.py"
'''

PLUGIN_TEST = r'''
class TestFilter(GitFilter):
    def smudge(self, content):
        content.set_text('test smudge\n' + content.get_text)

    def clean(self, content):
        text = content.get_text()
        if text.startswith('test smudge\n'):
            content.set_text(text[11:])
'''

class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def do_test_filter(self, filter, kw, path, expect):
        content = git_smudge.FileContent(path, None, False)
        clean = build_clean_text(**kw)
        content.set_text(clean)

        with self.subTest(t=clean, s=expect, p=path, **kw):
            filter.smudge(content)
            self.assertEqual(content.get_text(), expect)

            filter.clean(content)

            # First make sure that it actually changed the text
            self.assertNotEqual(content.get_text(), expect)
            self.assertEqual(content.get_text(), clean)

    def do_test_inserts(self, comment_style, path, comments, block):
        filter = git_smudge.InsertLineFilter({
            'after': r'(?s)im_start.*im_end',
            'insert': '\n'.join(TEST_LINES),
            'comment_style': comment_style,
            'block': block
        })
        filter.update_config()
        f = build_insert_test_smudge_block if block else build_insert_test_smudge_line
        for kw in INSERT_TESTS:
            smudge_expect = f(**kw, lines=TEST_LINES, comment=comments)
            self.do_test_filter(filter, kw, path, smudge_expect)


    def test_insert_block_c(self):
        self.do_test_inserts('css', Path('test.xxx'), git_smudge.COMMENT_C, True)

    def test_insert_block_sql(self):
        self.do_test_inserts('auto', Path('test.sql'), git_smudge.COMMENT_DDASH, True)

    def test_insert_line_xml(self):
        self.do_test_inserts('auto', Path('test.xml'), git_smudge.COMMENT_SGML, True)

    def test_insert_line_cpp(self):
        self.do_test_inserts('auto', Path('test.cpp'), git_smudge.COMMENT_DSLASH, True)

    def test_comment_out(self):
        filter = git_smudge.CommentOutFilter({
            'match': '(?s)im_start.*im_end'
        })
        filter.update_config()
        comment_styles = [
            ('test.py', git_smudge.COMMENT_HASH),
            ('test.xml', git_smudge.COMMENT_SGML),
            ('test.css', git_smudge.COMMENT_C),
        ]
        for i, kw in enumerate(INSERT_TESTS):
            fname, comments = comment_styles[i % len(comment_styles)]
            commented = build_comment_out_text(comment=comments, **kw)
            self.do_test_filter(filter, kw, Path(fname), commented)

    def get_filters_for_args(self, argv):
        p = argparse.ArgumentParser(description='')
        git_smudge.__main__.add_arguments_for_main(p)
        args = p.parse_args(argv)
        for filter in args.filters:
            filter.update_config()

        return args.filters

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp(prefix='git_smudge_unittest'))
        self.config_path = self.tempdir / 'config.toml'
        self.config_path.write_text(CONFIG_TOML, encoding='ascii')
        (self.tempdir / 'plugin-test.py').write_text(PLUGIN_TEST)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_config_1(self):

        cfg = config.Config(self.tempdir, self.config_path)
        cfg.load()
        self.assertSetEqual(set(cfg.filter_classes), {
            'test', 'simple', 'insertline', 'commentout'
        })
        TestFilter = cfg.filter_classes['test']

        nf = cfg.named_filters
        self.assertSetEqual(set(nf), {'filter1', 'filter2', 'filter3', 'foo', 'rootpy'})

        filter_list = nf['filter1']
        self.assertEqual(len(filter_list), 1)
        self.assertIsInstance(filter_list[0], git_smudge.SimpleFilter)

        filter_list = nf['filter2']
        self.assertEqual(len(filter_list), 3)
        self.assertIsInstance(filter_list[0], git_smudge.CommentOutFilter)
        self.assertIsInstance(filter_list[1], git_smudge.SimpleFilter)
        self.assertIsInstance(filter_list[2], git_smudge.InsertLineFilter)

        filter_list = nf['filter3']
        self.assertEqual(len(filter_list), 2)
        self.assertIsInstance(filter_list[0], git_smudge.CommentOutFilter)
        self.assertIsInstance(filter_list[1], git_smudge.SimpleFilter)

        pats = cfg.rule_patterns
        self.assertSetEqual(set(pats), {
            ('*', '*.c'), ('*', 'foo.c'), ('subdir', '*'), ('*', '*.txt'),
            ('*', 'special.c'), ('', '*.py')
        })

        for path, expect_filters in CONFIG_TEST_PATHS:
            with self.subTest(path=path):
                filters = cfg.get_filters_for_path(path)
                self.assertEqual([type(f).__name__ for f in filters], [f[0] for f in expect_filters])

if __name__ == '__main__':
    git_smudge.__main__.setup_logging(False)
    unittest.main()
