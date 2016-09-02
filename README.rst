===============================
Galaxy Updater
===============================

.. image:: https://img.shields.io/pypi/v/galaxy_updater.svg
        :target: https://pypi.python.org/pypi/galaxy_updater

.. image:: https://img.shields.io/travis/danrue/galaxy_updater.svg
        :target: https://travis-ci.org/danrue/galaxy_updater

Installation
------------

``pip install galaxy-updater``

Usage
-----

Given an example ansible-galaxy role file::

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
    - src: yatesr.timezone
    - src: carlosbuenosvinos.ansistrano-deploy
      version: 1.4.0

Find and print the latest version of each role listed in an ansible-galaxy role
file::

    $ galaxy-updater sample_requirements.yml 
    ansible-role-mysql: 1.9.0 -> 1.9.1
    ansible-role-apache: None -> 1.5.0
    ansible-role-php: 1.5.0 -> 1.7.3
    yatesr.timezone: None -> 1.0.0
    carlosbuenosvinos.ansistrano-deploy: 1.4.0 -> 1.10.0

Update the sample_requirements.yml file in place::

    $ galaxy-updater --inline sample_requirements.yml 
    ansible-role-mysql: 1.9.0 -> 1.9.1
    ansible-role-apache: None -> 1.5.0
    ansible-role-php: 1.5.0 -> 1.7.3
    yatesr.timezone: None -> 1.0.0
    carlosbuenosvinos.ansistrano-deploy: 1.4.0 -> 1.10.0

Use --yolo to leave unpinned dependencies unpinned::

    $ galaxy-updater --yolo sample_requirements.yml 
    ansible-role-mysql: 1.9.0 -> 1.9.1
    ansible-role-php: 1.5.0 -> 1.7.3
    carlosbuenosvinos.ansistrano-deploy: 1.4.0 -> 1.10.0
