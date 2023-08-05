#!/usr/bin/env python

"""Tests on the pydoni package file and folder structure."""

import pydoni
import re
import unittest
from os import chdir, remove
from os.path import dirname, join, abspath, expanduser, splitext, isfile, isdir, basename


class TestPackageStructure(unittest.TestCase):
    """
    Tests for pydoni package file and folder structure.
    """
    def test_test_data_folder(self):
        test_data_fpaths = pydoni.listfiles(path=join(tests_dir, 'test_data'),
                                            recursive=True,
                                            include_hidden=False)
        for fpath in test_data_fpaths:
            fpath_relative = re.sub(r'(.*?)(test_data\/)(.*)', r'\2\3', fpath)
            self.assertTrue(basename(fpath_relative).startswith('test_'),
                            msg=f'File "{fpath_relative}" does not start with "test_"')


tests_dir = dirname(abspath(__file__))
root_dir = dirname(tests_dir)
chdir(root_dir)

case = TestPackageStructure()

test_methods = [x for x in dir(case) if x.startswith('test_')]
for method in test_methods:
    getattr(case, method)()
