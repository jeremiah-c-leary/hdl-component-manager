Listing Components
==================

Use the **list** subcommand to view information about installed components.
It can also list information about available components stored in the component repo.

Example:  listing installed components
--------------------------------------

.. code-block:: bash

   $ hcm list

   [jcl - need some output]

Example:  listing upgrades available
------------------------------------

.. code-block:: bash

   $ hcm list --upgrades

   [jcl - need some output]

Example:  listing components available in component repo
--------------------------------------------------------

.. code-block:: bash

    $ hcm list --available

If multiple repos are listed in the **HCM_URL_PATHS** environment variable, then every component in all repos will be reported.

