from __future__ import print_function
import argparse
import os
import re
import subprocess
import sys

from distutils.version import LooseVersion
import ruamel.yaml
from builtins import object, str
from __init__ import __version__

class UnsupportedSrcError(Exception):
    def __init__(self, value="Unsupported src Error"):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GitTags(object):
    """ Retrieve git tags from a git url """

    def __init__(self, src):
        if 'git' in src:
            output = self._get_tags_from_git(src)
        elif 'file://' in src:
            output = self._get_tags_from_file(src)
        else:
            raise UnsupportedSrcError(
                "Unsupported source type: {0}".format(src))

        self.tags = re.findall(r'refs/tags/([\d\w\.]+)$',
                               output, re.MULTILINE)

    def latest(self):
        """ Return list of tags sorted by version number """

        if len(self.tags) < 1:
            return None
        return sorted(self.tags, key=LooseVersion)[-1]

    def _get_tags_from_git(self, src):
        """
           Retrieve tags from git url
           Uses subprocess to take advantage of local auth/keys settings
        """
        proc = subprocess.Popen(["git", "ls-remote", src],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        return proc.communicate()[0]

    def _get_tags_from_file(self, src):
        """ Testing interface """
        src_path = src.split('//')[-1]
        with open(src_path, 'r') as f:
            return f.read()

class Updater(object):
    """ Find latest version of each role """

    def __init__(self, requirement_file):
        self.requirement_file = requirement_file
        with open(requirement_file, 'r') as f:
            self.reqs = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)

    def _pattern_in_src(self, src, pattern):
        for pat in pattern:
            if pat in src:
                return True
        return False

    def find_latest_versions(self, replace_inline=False,
                             update_unversioned=True,
                             include_pattern=[],
                             exclude_pattern=[]):
        """
          Return a list of available updates

          If replace_inline is set, actually modify the original
          requirements file.
        """
        output = []
        for i, req in enumerate(self.reqs):
            assert req['src'], "Error, src key not found in {0}".format(req)
            src = req['src']
            short_name = src.split('/')[-1].split('.')[0]
            version = req.get('version')
            g = GitTags(src)

            if not g.latest():
                continue
            if not version and not update_unversioned:
                continue
            if (include_pattern and
                    not self._pattern_in_src(src, include_pattern)):
                continue
            if exclude_pattern and self._pattern_in_src(src, exclude_pattern):
                continue

            if ((not version) or
                    (LooseVersion(version) < LooseVersion(g.latest()))):
                # If version is not set, suggest the latest version
                output.append("{0}: {1} -> {2}".format(
                    short_name, version, g.latest()))
                if replace_inline:
                    self.reqs[i]["version"] = g.latest()

        if replace_inline:
            # Modify existing file
            with open(self.requirement_file, 'w') as f:
                f.write(ruamel.yaml.dump(self.reqs, Dumper=ruamel.yaml.RoundTripDumper))

        return output

def main():
    parser = argparse.ArgumentParser(
        description='Update ansible-galaxy requirements file')
    parser.add_argument('--inline', help="Edit requirements file in-place",
                        action='store_true')
    parser.add_argument('--yolo', help="Ignore unversioned roles",
                        action='store_true')
    parser.add_argument('--include',
                        help="Only include roles src matching pattern",
                        dest='include_pattern',
                        default=[],
                        action='append')
    parser.add_argument('--exclude',
                        help="Only include roles src matching pattern",
                        dest='exclude_pattern',
                        default=[],
                        action='append')
    parser.add_argument('--version',
                        action='version',
                        version='galaxy-updater {0}'.format(__version__))
    parser.add_argument('requirement_file', help="ansible-galaxy yaml file")
    args = parser.parse_args()

    if not os.path.isfile(args.requirement_file):
        parser.print_help()
        sys.exit(1)
    u = Updater(args.requirement_file)
    for line in u.find_latest_versions(replace_inline=args.inline,
                                       update_unversioned=not args.yolo,
                                       include_pattern=args.include_pattern,
                                       exclude_pattern=args.exclude_pattern):
        if args.yolo and "None" in line:
            continue
        print(line)

if __name__ == '__main__':
    main()
