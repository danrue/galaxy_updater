===============================
Galaxy Updater
===============================

.. image:: https://img.shields.io/pypi/v/galaxy_updater.svg
        :target: https://pypi.python.org/pypi/galaxy_updater

.. image:: https://img.shields.io/travis/danrue/galaxy_updater.svg
        :target: https://travis-ci.org/danrue/galaxy_updater


Retrieve the latest version tags for all of your ansible-galaxy requirements.

Installation
------------

``pip install galaxy_updater``

Usage
-----

Find the latest version of each role listed in an ansible-galaxy role file::

    $ galaxy_updater sample_requirements.yml 
    ansible-role-mysql: 1.9.0 -> 1.9.1
    ansible-role-apache: None -> 1.5.0
    ansible-role-php: 1.5.0 -> 1.7.3


Given an ansible-galaxy role file::

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

