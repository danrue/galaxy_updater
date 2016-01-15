#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_galaxy_updater
----------------------------------

Tests for `galaxy_updater` module.
"""
from builtins import object

from galaxy_updater import galaxy_updater


class TestGalaxy_updater(object):

    def test_000_something(self):
        u = galaxy_updater.updater("tests/test_files/1_requirements.yml")
        output = u.find_latest_versions()
        assert len(output) == 5


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
