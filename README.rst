HDL Component Manager (HCM)
===========================

Manage HDL code as components so they can shared as IP.

.. image:: https://img.shields.io/github/tag/jeremiah-c-leary/hdl-component-manager.svg?style=flat-square
   :target: https://github.com/jeremiah-c-leary/hdl-component-manager
   :alt: Github Release
.. image:: https://img.shields.io/pypi/v/hcm.svg?style=flat-square
   :target: https://pypi.python.org/pypi/hcm
   :alt: PyPI Version
.. image:: https://img.shields.io/travis/jeremiah-c-leary/hdl-component-manager/master.svg?style=flat-square
   :target: https://travis-ci.org/jeremiah-c-leary/hcm-component-manager
   :alt: Build Status
.. image:: https://img.shields.io/codecov/c/github/jeremiah-c-leary/hdl-component-manager/master.svg?style=flat-square
   :target: https://codecov.io/github/jeremiah-c-leary/hdl-component-manager
   :alt: Test Coverage
.. image:: https://img.shields.io/readthedocs/vsg.svg?style=flat-square
   :target: http://hdl-component-manager.readthedocs.io/en/latest/index.html
   :alt: Read The Docs
.. image:: https://api.codacy.com/project/badge/Grade/42744dca97544824b93cfc99e8030063
   :target: https://www.codacy.com/app/jeremiah-c-leary/hdl-component-manager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jeremiah-c-leary/hdl-component-manager&amp;utm_campaign=Badge_Grade
   :alt: Codacy
.. image:: https://api.codeclimate.com/v1/badges/97a72b806d6919dbcfa9/maintainability
   :target: https://codeclimate.com/github/jeremiah-c-leary/hdl-component-manager/maintainability
   :alt: Maintainability

Table of Contents
-----------------

*   `Overview`_
*   `Key Benefits`_
*   `Key Features`_
*   `Installation`_
*   `Usage`_
*   `Documentation`_
*   `Contributing`_

Overview
--------

HCM was created after a frustrating attempt to merge changes from one program to another.
Even after carefully performing the merge, there were issues.

It was turning into a nightmare just to pass updates between multiple concurrently running programs.
I was inspired by PIP, and how easy it is to install python packages.
I wanted to bring that same level of ease to HDL design.

Key Benefits
------------

*   Provides a method to control versions of IP
*   Controls the distribution of HDL code
*   Follows the Major.Minor.Patch method of version control
*   Language independent (VHDL, Verilog, System Verilog)
*   Can be used to control vendor IP

Key Features
------------

*   Works with SVN repositories
*   Automates publishing of code to a central location
*   Automates installing and upgrading of code
*   Supports multiple IP repositories
*   Supports dependencies between components

Installation
------------

You can get the latest released version of HCM via **pip**.

.. code-block:: bash

   pip install hcm

The latest development version can be cloned...

.. code-block:: bash

  git clone https://github.com/jeremiah-c-leary/hdl-component-manager.git

...and then installed locally...

.. code-block:: bash

  python setup.py install

.. include:: https://github.com/jeremiah-c-leary/hdl-component-manager/blob/master/docs/source/usage.rst

Documentation
-------------

All documentation for HCM is hosted at `read-the-docs <http://hdl-component-manager.readthedocs.io/en/latest/index.html>`_.

Contributing
------------

I welcome any contributions to this project.
No matter how small or large.

There are several ways to contribute:

*   Bug reports
*   Code base improvements
*   Feature requests
*   Pull requests

Please refer to the documentation hosted at `read-the-docs <http://hdl-component-manager.readthedocs.io/en/latest/index.html>`_ for more details on contributing.
