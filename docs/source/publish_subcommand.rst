Publishing Components
=====================

Use the **publish** subcommand to add components to the component repo.
If there is only one path defined in the **HCM_URL_PATHS** environment variable, then the *--url* argument is optional.
Otherwise HCM will indicate the *--url* argument is required, as it will not know which repo to store the 

.. code-block:: bash

  > hcm publish I2C_CONTROL 2.1.0

Example:  Publishing a new component
------------------------------------

.. code-block:: bash

   $ hcm publish temp_ctrl 1.0.0 --url http://svn/acme/project1/components

   [jcl - need some output]

HCM will create a configuration file named **hcm.yaml**.
This file will contain information related to the component.

HCM will delete the current component directory and point to the just published version.

Example:  Publishing an update to a component
---------------------------------------------

If the **hcm.yaml** file exists, then publishing does not require the *--url* argument.

.. code-block:: bash

   $ hcm publish temp_ctrl 1.1.0

   [jcl - need some output]

HCM will update the **hcm.yaml** file with the new version before it is committed to the component repo.
HCM will delete the current component directory and point to the just published version.

hcm.yaml file
-------------

The hcm.yaml file looks like this:

.. code-block:: yaml

   hcm :
     url : http://svn/acme/project1/components
     name : temp_ctrl
     version : 1.1.0

