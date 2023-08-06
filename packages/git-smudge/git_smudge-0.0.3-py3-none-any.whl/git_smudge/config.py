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

import os
import copy
import subprocess
from pathlib import Path
from ktpanda.fileutils import load_json, save_json

def run_git(cmd, check=True):
    return subprocess.run(
        ['git'] + cmd, stdout=subprocess.PIPE, check=check,
        encoding='utf8', errors='surrogateescape')

def get_path(relpath) -> Path:
    '''Return a `Path` object pointing to a file within the .git directory'''
    return Path(run_git(['rev-parse', '--git-path', relpath]).stdout.rstrip('\n'))

class JSONDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f'Key {attr} is not present') from None

class Config:
    def __init__(self, path):
        self.path = path
        self.config = JSONDict()
        self.last_loaded = JSONDict()

    @classmethod
    def from_git(cls):
        return cls(get_path('git-smudge.config.json'))

    def load(self):
        data = load_json(self.path, object_pairs_hook=JSONDict)
        if data is None:
            data = JSONDict()
        self.data = data
        self.last_loaded = copy.deepcopy(data)

    def save(self, force=False):
        if force or self.data != self.last_loaded:
            save_json(self.path, self.config)
            self.last_loaded = copy.deepcopy(self.data)
