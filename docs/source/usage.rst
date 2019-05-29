Usage
=====

HCM can be invoked by issuing **hcm** at the command line prompt:

.. code-block:: bash

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
    
HCM has four subcommands:  create, install, list, and publish.

create
------

Use the **create** subcommand to create a new component repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm create -h
    usage: hcm create [-h] url
    
    positional arguments:
      url         location to create the base component repo
    
    optional arguments:
      -h, --help  show this help message and exit

install
-------

Use the **install** subcommand to add or upgrade a componet from the component repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ bin/hcm install -h
    usage: hcm install [-h] [--url URL] component version
    
    positional arguments:
      component   Component name to install
      version     Major.Minor.Patch version of component to install, or latest to
                  grab the latest version.
    
    optional arguments:
      -h, --help  show this help message and exit
      --url URL   location of component directory in repo

list
----

Use the **list** subcommand to check the versions of components you have installed.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm list -h
    usage: hcm list [-h] [--upgrades] [--all]
    
    optional arguments:
      -h, --help  show this help message and exit
      --upgrades  Lists upgrades for currently installed components
      --all       Includes directories that are not under HCM control

publish
-------

Use the **publish** subcommand to push a version of a component to the component repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm publish -h
    usage: hcm publish [-h] -m M [--url URL] component version
    
    positional arguments:
      component   Component name to publish
      version     Major.Minor.Patch version to publish
    
    optional arguments:
      -h, --help  show this help message and exit
      -m M        Commit message
      --url URL   Base URL of the component repository

Environment Variables
---------------------

HCM will use the **HCM_URL_PATHS** environment variable as a replacement for the **--url** command line option.
HCM uses the paths in the variable to know which component repos to interact with.

.. NOTE::  Only one URL path is currently supported
