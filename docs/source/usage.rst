Usage
=====

HCM can be invoked with:

.. code-block:: bash

    $ hcm
    usage: hcm [-h] {create,list,publish,update} ...
    
    Provides configuration management for HDL components.
    
    positional arguments:
      {create,list,publish,update}
        create              creates a component repo
        install             adds a component from the component repo
        list                lists components and their versions
        publish             Adds components to the component repo
        update              Updates a component to the requested version
    
    optional arguments:
      -h, --help            show this help message and exit

HCM has five subcommands:  create, install, list, publish, and update.

create
------

The create subcommand is used when you want to create a new component repository.
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

The install subcommand is used when you want to add a component from the component repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ bin/hcm install -h
    usage: hcm install [-h] [--version VERSION] url
    
    positional arguments:
      url                location of component in component repo
    
    optional arguments:
      -h, --help         show this help message and exit
      --version VERSION  Major.Minor.Patch version of component to update to

list
----

The list subcommand is used when you want to check which versions of components you have installed.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm list -h
    usage: hcm list [-h] [--upgrades UPGRADES] [--available AVAILABLE]
    
    optional arguments:
      -h, --help            show this help message and exit
      --upgrades UPGRADES   Lists upgrades for currently installed
                            components
      --available AVAILABLE
                            Lists available components stored in repo

publish
-------

The publish subcommand is used when you want to push a version of a component to the component repository.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm publish -h
    usage: hcm publish [-h] component version
    
    positional arguments:
      component   Component name to publish
      version     Major.Minor.Patch version to publish
    
    optional arguments:
      -h, --help  show this help message and exit


update
------

The update subcommand is used when you want to pull in a newer version of the current component.
The arguments for the subcommand can be listed using the *-h* option:

.. code-block:: bash

    $ hcm update -h
    usage: hcm update [-h] component version
    
    positional arguments:
      component   Component name to update
      version     Major.Minor.Patch version of component to update to
    
    optional arguments:
      -h, --help  show this help message and exit


Environment Variables
---------------------

HCM requires the **HCM_URL_PATHS** environment variable is set before using the install, list, publish, or update subcommands.
HCM uses the paths in the variable to know which component repos to interact with.
