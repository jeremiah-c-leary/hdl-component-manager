Installing Components
=====================

Use the **install** subcommand to bring in a new component that is not part of your current working copy.
The URL path to the component and the version are required to install a new component.
This can be found using a repository browser or the **list** subcommand.

Example:  installing a spi master controller
--------------------------------------------

After viewing the component repository, we decide to pull in version 3.0.0 of a SPI_MASTER_CONTROLLER.

.. code-block:: bash

   $ hcm install SPI_MASTER_CONTROL --version 3.0.0

HCM will use the paths in the **HCM_URL_PATHS** environment variable and search for the component name.
HCM will then check if the version exists.
If the **version** argument is not used, then the latest version of the component will be installed.

Example:  installing latest version of a Temperature Sensor
-----------------------------------------------------------

.. code-block:: bash

   $ hcm install temp_ctrl

