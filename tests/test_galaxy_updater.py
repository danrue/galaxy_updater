#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_galaxy_updater
----------------------------------

Tests for `galaxy_updater` module.
"""
from builtins import object

from galaxy_updater import galaxy_updater
import hashlib
import os
import shutil


class TestGalaxy_updater(object):

    def test_000_default(self):
        """ Normal Run - 5 changes """
        u = galaxy_updater.updater("tests/test_files/1_requirements.yml")
        output = u.find_latest_versions()
        assert len(output) == 5

    def test_001_inline(self):
        """ Test 4 inline changes """
        inline = True
        yolo = False
        testfile = "tests/test_files/2_requirements.yml"
        testfile_bak = "{0}.bak".format(testfile)
        shutil.copyfile(testfile, testfile_bak)
        u = galaxy_updater.updater(testfile)
        output = u.find_latest_versions(replace_inline = inline,
                                        update_unversioned = not yolo)

        print(output)
        assert len(output) == 4
        assert (hashlib.md5(open(testfile, 'rb').read()).hexdigest() == 
                "82111e45e03c488120afa64dc890bf3f")

        shutil.copyfile(testfile_bak, testfile)
        os.remove(testfile_bak)


    def test_002_inline_yolo(self):
        """ Test 3 inline changes, ignoring unversioned (yolo) """
        inline = True
        yolo = True
        testfile = "tests/test_files/2_requirements.yml"
        testfile_bak = "{0}.bak".format(testfile)
        shutil.copyfile(testfile, testfile_bak)
        u = galaxy_updater.updater(testfile)
        output = u.find_latest_versions(replace_inline = inline,
                                        update_unversioned = not yolo)
        assert len(output) == 3
        assert (hashlib.md5(open(testfile, 'rb').read()).hexdigest() == 
                "63b7895e07d4973609018bce6fc8628b")

        shutil.copyfile(testfile_bak, testfile)
        os.remove(testfile_bak)

    def test_003_noupdates(self):
        """ Test no updates """
        u = galaxy_updater.updater("tests/test_files/3_requirements.yml")
        output = u.find_latest_versions(replace_inline=True)
        assert len(output) == 0

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
