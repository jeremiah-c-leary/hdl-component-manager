Uninstalling Components
=======================

Use the **uninstall** subcommand to remove components from your current working copy.

Example:  Uninstalling a Component
----------------------------------

We have decided we no longer need the component bishop.

.. code-block:: bash

   $ hcm uninstall bishop
   INFO:Uninstalled component bishop

The component must be committed for the change to be permanent:

.. code-block:: bash

   $ svn commit -m "Removed bishop component"

Example:  Uninstalling an externalled component
-----------------------------------------------

HCM will modify the svn:externals attribute and perform an update.

.. code-block:: bash

   $ hcm uninstall rook
   INFO:Uninstalled component rook

The parent directory must be committed for the change to be permanent:

.. code-block:: bash

   $ svn commit . -m "Removed bishop component"

