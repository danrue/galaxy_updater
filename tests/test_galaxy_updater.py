#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_galaxy_updater
----------------------------------

Tests for `galaxy_updater` module.
"""
import hashlib
import os
import shutil
from galaxy_updater import galaxy_updater
from builtins import object


class TestGalaxyUpdater(object):
    """ Test galaxy-updater """

    def test_000_default(self):
        """ Normal Run - 5 changes """
        updater = galaxy_updater.Updater("tests/test_files/1_requirements.yml")
        output = updater.find_latest_versions()
        assert output == ['ansible-role-mysql: 0.0.1 -> 1.9.1',
                          'ansible-role-apache: 0.0.1 -> 1.5.0',
                          'ansible-role-jenkins: 0.0.1 -> 1.2.8',
                          'ansible-role-php: 0.0.1 -> 1.7.3',
                          'ansible-role-1-tag: 0.0.1 -> 1.0.0']

    def test_001_inline(self):
        """ Test 4 inline changes """
        inline = True
        yolo = False
        testfile = "tests/test_files/2_requirements.yml"
        testfile_bak = "{0}.bak".format(testfile)
        shutil.copyfile(testfile, testfile_bak)
        updater = galaxy_updater.Updater(testfile)
        output = updater.find_latest_versions(replace_inline=inline,
                                              update_unversioned=not yolo)

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
        updater = galaxy_updater.Updater(testfile)
        output = updater.find_latest_versions(replace_inline=inline,
                                              update_unversioned=not yolo)
        assert len(output) == 3
        assert (hashlib.md5(open(testfile, 'rb').read()).hexdigest() ==
                "63b7895e07d4973609018bce6fc8628b")

        shutil.copyfile(testfile_bak, testfile)
        os.remove(testfile_bak)

    def test_003_noupdates(self):
        """ Test no updates """
        updater = galaxy_updater.Updater("tests/test_files/3_requirements.yml")
        output = updater.find_latest_versions(replace_inline=True)
        assert len(output) == 0

    def test_004_includes(self):
        """ Test --include """
        includes = ['mysql', 'apache']
        updater = galaxy_updater.Updater("tests/test_files/1_requirements.yml")
        output = updater.find_latest_versions(include_pattern=includes)
        assert output == ['ansible-role-mysql: 0.0.1 -> 1.9.1',
                          'ansible-role-apache: 0.0.1 -> 1.5.0']

    def test_005_excludes(self):
        """ Test --exclude """
        excludes = ['mysql', 'apache']
        updater = galaxy_updater.Updater("tests/test_files/1_requirements.yml")
        output = updater.find_latest_versions(exclude_pattern=excludes)
        assert output == ['ansible-role-jenkins: 0.0.1 -> 1.2.8',
                          'ansible-role-php: 0.0.1 -> 1.7.3',
                          'ansible-role-1-tag: 0.0.1 -> 1.0.0']

    def test_004_includes_excludes(self):
        """ Test --include with --exclude """
        includes = ['ansible', 'role', 'php']
        excludes = ['mysql', 'apache']
        updater = galaxy_updater.Updater("tests/test_files/1_requirements.yml")
        output = updater.find_latest_versions(include_pattern=includes,
                                              exclude_pattern=excludes)
        assert output == ['ansible-role-jenkins: 0.0.1 -> 1.2.8',
                          'ansible-role-php: 0.0.1 -> 1.7.3',
                          'ansible-role-1-tag: 0.0.1 -> 1.0.0']


