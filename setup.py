#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='galaxy-updater',
    version='0.0.1',
    description=('Retrieve the latest version tags for all of your '
                 'ansible-galaxy dependencies.'),
    long_description=readme + '\n\n' + history,
    author="Dan Rue",
    author_email='drue@therub.org',
    url='https://github.com/danrue/galaxy_updater',
    packages=[
        'galaxy_updater',
    ],
    package_dir={'galaxy_updater':
                 'galaxy_updater'},
    include_package_data=True,
    install_requires=['pyyaml', 'future'],
    license="BSD",
    keywords='ansible-galaxy ansible galaxy requirements.yml',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['pytest'],

    entry_points={
        'console_scripts': [
            'galaxy_updater=galaxy_updater.galaxy_updater:main',
        ],
    },

)
