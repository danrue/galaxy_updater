Galaxy Updater
==============

[<img src="https://img.shields.io/pypi/danrue/galaxy_updater.svg">](https://pypi.python.org/pypi/galaxy_updater)

[<img src="https://img.shields.io/travis/danrue/galaxy_updater.svg">](https://travis-ci.org/danrue/galaxy_updater)

Installation
------------

```bash
pip install galaxy_updater
```

Example Usage
-------------

Given an ansible-galaxy role file:

```bash
    $ cat sample_requirements.yml 
    ---
    - src: https://github.com/geerlingguy/ansible-role-mysql.git 
      name: ansible-role-mysql
      version: 1.9.0
    - src: https://github.com/geerlingguy/ansible-role-apache.git 
      name: ansible-role-apache
    - src: https://github.com/geerlingguy/ansible-role-jenkins.git 
      name: ansible-role-jenkins
      version: 1.2.8
    - src: https://github.com/geerlingguy/ansible-role-php.git 
      name: ansible-role-php
      version: 1.5.0
```

Find the latest version of each role:

```bash
    $ galaxy_updater sample_requirements.yml 
    ansible-role-mysql: 1.9.0 -> 1.9.1
    ansible-role-apache: None -> 1.5.0
    ansible-role-php: 1.5.0 -> 1.7.3
```
