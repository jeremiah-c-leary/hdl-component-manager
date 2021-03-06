Usage
=====

HCM can be invoked by issuing **hcm** at the command line prompt:

.. code-block:: bash

    $ hcm
    usage: hcm [-h]
               {browse,create,download,install,uninstall,list,publish,show,validate,version}
               ...
    
    Provides configuration management for HDL components.
    
    positional arguments:
      {browse,create,download,install,uninstall,list,publish,show,validate,version}
        browse              List components available for installation.
        create              Creates a component repo
        download            Downloads components without installing them.
        install             Adds a component from the component repo
        uninstall           Removes installed components
        list                Lists components and their versions
        publish             Adds components to the component repo
        show                Displays information about installed components
        validate            Verifies manifest of installed component
        version             Displays HCM version information
    
    optional arguments:
      -h, --help            show this help message and exit

HCM has ten subcommands:  browse, create, download, install, uninstall, list, publish, show, validate, and version.

browse
------

Use the **browse** subcommand to list components available for installation.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm browse -h
    usage: hcm browse [-h] [component]
    
    positional arguments:
      component   Component to browse
    
    optional arguments:
      -h, --help  show this help message and exit

create
------

Use the **create** subcommand to create a component directory in the repository.
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

Use the **install** subcommand to add or upgrade a component from a repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ bin/hcm install -h
    usage: hcm install [-h] [--version VERSION] [--url URL] [--force] [--external]
                       [--dependencies] [--upgrade]
                       component
    
    positional arguments:
      component          Component name to install
    
    optional arguments:
      -h, --help         show this help message and exit
      --version VERSION  Major.Minor.Patch version of component to install.
      --url URL          location of component directory in repo
      --force            Install component ignoring any local changes
      --external         Install as an external
      --dependencies     Install dependencies
      --upgrade          Upgrade dependencies to latest version

uninstall
---------

Use the **uninstall** subcommand to remove installed components.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm uninstall -h
    usage: hcm uninstall [-h] component
    
    positional arguments:
      component   Installed Component name to install
    
    optional arguments:
      -h, --help  show this help message and exit

list
----

Use the **list** subcommand to check the versions of components you have installed.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm list -h
    usage: hcm list [-h] [--all]
    
    optional arguments:
      -h, --help  show this help message and exit
      --all       Includes directories that are not under HCM control

publish
-------

Use the **publish** subcommand to push a version of a component to a repository.
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

show
----

Use the **show** subcommand to display information about an installed component.
The arguments for the subcommand can be listed using the *-h* options:

.. code-block:: bash

    $ hcm show -h
    usage: hcm show [-h] [--manifest] [--upgrades] [--updates] [--modifications]
                    component
    
    positional arguments:
      component        Component to display information
    
    optional arguments:
      -h, --help       show this help message and exit
      --manifest       Displays manifest for all files in component
      --upgrades       Lists upgrade versions and their log entries
      --updates        Lists versions with newer publishes and their log entries
      --modifications  Lists committed modifications for component

validate
--------

Use the **validate** subcommand to compare the component manifest against what is currently installed.
The arguments for the subcommand can be listed using the *-h* options:

.. code-block:: bash

    $ hcm validate -h
    usage: hcm validate [-h] [--report] component
    
    positional arguments:
      component   Component to display information
    
    optional arguments:
      -h, --help  show this help message and exit
      --report    Reports differences

version
-------

Use the **version** subcommand to display version information for HCM.

Environment Variables
---------------------

HCM will use the **HCM_URL_PATHS** environment variable as a replacement for the **--url** command line option.
HCM uses the paths in the variable to know which component repositories to interact with.
