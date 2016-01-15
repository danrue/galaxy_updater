from __future__ import print_function
from builtins import object
import argparse
import os
import re
import subprocess
import sys
import yaml
from distutils.version import LooseVersion

class UnsupportedSrcError(Exception):
    def __init__(self, value = "Unsupported src Error"):
        self.value = value
    def __str__(self):
        return repr(self.value)

class git_tags(object):
    def __init__(self, src):
        if 'git' in src:
            output = self._get_tags_from_git(src)
        elif 'file://' in src:
            output = self._get_tags_from_file(src)
        else:
            raise UnsupportedSrcError(
                  "Unsupported source type: {}".format(src))

        self.tags = re.findall(r'refs/tags/([\d+.]+)$', output, re.MULTILINE)

    def latest(self):
        return sorted(self.tags, key=LooseVersion)[-1]

    def _get_tags_from_git(self, src):
        p = subprocess.Popen(["git", "ls-remote", src], 
                             stdout=subprocess.PIPE)
        return p.communicate()[0]

    def _get_tags_from_file(self, src):
        src_path = src.split('//')[-1]
        with open(src_path, 'r') as f:
            return f.read()

class updater(object):
    def __init__(self, requirement_file):
        with open(requirement_file, 'r') as f:
            self.reqs = yaml.safe_load(f)

    def find_latest_versions(self):
        output = []
        for req in self.reqs:
            assert req['src'], "Error, src key not found in {}".format(req)
            src = req['src']
            short_name = src.split('/')[-1].split('.')[0]
            version = req.get('version')
            g = git_tags(src)

            if ( (not version) or
                 (LooseVersion(version) < LooseVersion(g.latest())) ):
                # If version is not set, suggest the latest version
                output.append("{}: {} -> {}".format( 
                               short_name, version, g.latest()))
        return output

def main():
    parser = argparse.ArgumentParser(
             description='Update ansible-galaxy requirements file')
    parser.add_argument('requirement_file', help="ansible-galaxy yaml file")
    args = parser.parse_args()

    if not os.path.isfile(args.requirement_file):
        parser.print_help()
        sys.exit(1)
    u = updater(args.requirement_file)
    for line in u.find_latest_versions():
        print(line)

if __name__ == '__main__':
    main()
