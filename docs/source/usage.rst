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
        list                lists components and their versions
        publish             Adds components to the component repo
        update              Updates a component to the requested version
    
    optional arguments:
      -h, --help            show this help message and exit


create
------

.. code-block:: bash

    $ hcm create -h
    usage: hcm create [-h] url
    
    positional arguments:
      url         location to create the base component repo
    
    optional arguments:
      -h, --help  show this help message and exit

list
----

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

.. code-block:: bash

    $ hcm update -h
    usage: hcm update [-h] component version
    
    positional arguments:
      component   Component name to update
      version     Major.Minor.Patch version of component to update to
    
    optional arguments:
      -h, --help  show this help message and exit

