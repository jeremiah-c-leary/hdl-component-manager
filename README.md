HDL Component Manager (HCM)
===========================

Manage HDL code as components so they can shared as IP.

<div align="center">
  <!-- github release -->
  <a href="https://github.com/jeremiah-c-leary/hdl-component-manager">
    <img src="https://img.shields.io/github/tag/jeremiah-c-leary/hdl-component-manager.svg?style=flat-square"
      alt="Github Release" />
  </a>
  <!-- PyPI version -->
  <a href="https://pypi.python.org/pypi/hcm">
    <img src="https://img.shields.io/pypi/v/hcm.svg?style=flat-square"
      alt="PyPI Version" />
  </a>
  <!-- Build Status -->
  <a href="https://travis-ci.org/jeremiah-c-leary/hcm-component-manager">
    <img src="https://img.shields.io/travis/jeremiah-c-leary/hdl-component-manager/master.svg?style=flat-square"
      alt="Build Status" />
  </a>
  <!-- Test Coverage -->
  <a href="https://codecov.io/github/jeremiah-c-leary/hdl-component-manager">
    <img src="https://img.shields.io/codecov/c/github/jeremiah-c-leary/hdl-component-manager/master.svg?style=flat-square"
      alt="Test Coverage" />
  </a>
  <!-- Read The Docs -->
  <a href="http://hdl-component-manager.readthedocs.io/en/latest/index.html">
    <img src="https://img.shields.io/readthedocs/vsg.svg?style=flat-square"
      alt="Read The Docs" />
  </a>
  <!-- Codacy -->
  <a class="badge-align" href="https://www.codacy.com/app/jeremiah-c-leary/hdl-component-manager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jeremiah-c-leary/hdl-component-manager&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/42744dca97544824b93cfc99e8030063"
      alt="Codacy" />
  </a>
</div>

HDL Component Manager (HCM) provides a package manager for HDL languages.

Table of Contents
-----------------

<!--ts-->

*   [Overview](#Overview)
*   [Key Benefits](#Key-Benefits)
*   [Key Features](#Key-Features)
*   [Installation](#Installation)
*   [Usage](#Usage)
*   [Documentation](#Documentation)
*   [Contributing](#Contributing)

<!--te-->

Overview
--------

HCM was created after a frustrating attempt to merge changes from one program to another.
Even after carefully performing the merge, there were issues.
We fixed an issue with a component shared between programs, and wanted to push the change back to another program.
This would have required another merge.
SVN can handle it, put it gets really messy to do it manually.

This was turning into a nightmare just to pass updates between multiple concurrently running programs.
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

Installation
------------

You can get the latest released version of HCM via **pip**.

``` bash
pip install hcm
```

The latest development version can be cloned...

``` bash
git clone https://github.com/jeremiah-c-leary/hdl-component-manager.git
```

...and then installed locally...

``` bash
python setup.py install
```

Usage
-----

HCM is a command line tool.
It can be invoked with:

``` bash
$ hcm
usage: hcm [-h] {create,install,list,publish} ...

Provides configuration management for HDL components.

positional arguments:
  {create,install,list,publish}
    create              creates a component repo
    install             adds a component from the component repo
    list                lists components and their versions
    publish             Adds components to the component repo

optional arguments:
  -h, --help            show this help message and exit
```

HCM has four subcommands:  create, install, list, and publish.

### create

Use the **create** subcommand to create a new component repository.
The arguments for the subcommand can be listed using the *-h* option:

``` bash
$ hcm create -h
usage: hcm create [-h] url

positional arguments:
  url         location to create the base component repo

optional arguments:
  -h, --help  show this help message and exit
```

### install

Use the **install** subcommand to add or upgrade a componet from the component repository.
The arguments for the subcommand can be listed using the *-h* option:

``` bash
$ bin/hcm install -h
usage: hcm install [-h] [--url URL] component version

positional arguments:
  component   Component name to install
  version     Major.Minor.Patch version of component to install, or latest to
              grab the latest version.

optional arguments:
  -h, --help  show this help message and exit
  --url URL   location of component directory in repo
```

### list

Use the **list** subcommand to check the versions of components you have installed.
The arguments for the subcommand can be listed using the *-h* option:

``` bash
$ hcm list -h
usage: hcm list [-h] [--upgrades] [--all]

optional arguments:
  -h, --help  show this help message and exit
  --upgrades  Lists upgrades for currently installed components
  --all       Includes directories that are not under HCM control
```

### publish

Use the **publish** subcommand to push a version of a component to the component repository.
The arguments for the subcommand can be listed using the *-h* option:

``` bash
$ hcm publish -h
usage: hcm publish [-h] -m M [--url URL] component version

positional arguments:
  component   Component name to publish
  version     Major.Minor.Patch version to publish

optional arguments:
  -h, --help  show this help message and exit
  -m M        Commit message
  --url URL   Base URL of the component repository
```

Documentation
-------------

All documentation for HCM is hosted at [read-the-docs](http://hdl-component-manager.readthedocs.io/en/latest/index.html)

Contributing
------------

I welcome any contributions to this project.
No matter how small or large.

There are several ways to contribute:

*   Bug reports
*   Code base improvements
*   Feature requests
*   Pull requests

Please refer to the documentation hosted at [read-the-docs](http://hdl-component-manager.readthedocs.io/en/latest/index.html) for more details on contributing.
