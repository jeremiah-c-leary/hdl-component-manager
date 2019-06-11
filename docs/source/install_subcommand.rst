Installing Components
=====================

Use the **install** subcommand to add a component to your current working copy.
The URL path to the component and the version are required to install a new component.
This can be found using a repository browser or the **svn ls** subcommand.

Example:  Installing a Component
--------------------------------

After viewing the component repository, we decide to pull in version 3.0.0 of the rook component.

.. code-block:: bash

   $ hcm install rook 3.0.0
   INFO:Installing component rook version 3.0.0
   INFO:Validating all files for component rook are committed.
   INFO:Removing local component directory
   INFO:Installation complete

HCM will use the paths in the **HCM_URL_PATHS** environment variable.
It will search each path for a matching component name and version.

Example:  Installing the latest version of a component
------------------------------------------------------

If the version argument is left blank, then HCM will install the latest version of the component.

.. code-block:: bash

   $ hcm install rook
   INFO:Installing component rook
   INFO:Validating all files for component rook are committed.
   INFO:Removing local component directory
   INFO:Installation complete

Example:  installing component when files under the component directory are not committed
-----------------------------------------------------------------------------------------

HCM validates every file under the local component directory is checked in.
If this is not the case, then HCM will not install over the existing directory.

.. code-block:: bash

   $ ../../bin/hcm install rook 3.0.0
   INFO:Installing component rook version 3.0.0
   INFO:Validating all files for component rook are committed.
   ERROR:The following files must be committed or removed:
   M       rook/rtl/rook.vhd

This behavior can be overridden by using the **--force** command line option.

.. code-block:: bash

   $ hcm install rook 3.0.0 --force
   INFO:Installing component rook version 3.0.0
   INFO:Removing local component directory
   INFO:Installation complete

Example:  installing from an external repo
------------------------------------------

When installing from an external repo, HCM must use the **svn export** command.

.. code-block:: bash

   $ hcm install pawn 1.0.0 --url http://svn/external_repo/blocks
   INFO:Installing component pawn version 1.0.0
   INFO:Validating all files for component pawn are committed.
   INFO:Removing local component directory
   INFO:Installation complete

Performing an **svn status** command shows a new directory has been created.

.. code-block:: bash

   $ svn status
   ?       pawn

The directory must be added using the **svn add** command...

.. code-block:: bash

   $ svn add pawn
   A         pawn
   A         pawn/hcm.json
   A         pawn/rtl
   A         pawn/rtl/pawn.vhd

... and then committed.

.. code-block:: bash

   $ svn commit pawn

.. NOTE:: The last two steps are left to the user to perform.

Example: Installing using an external
-------------------------------------

HCM can install components using externals.
An external is a essentially a pointer to directory in a repository.

.. code-block:: bash

   $ hcm install pawn 3.0.0 --external
   INFO:Installing component pawn version 3.0.0
   INFO:Validating all files for component pawn are committed.
   INFO:Removing local component directory
   INFO:Updating externals
   INFO:Installation complete

Checking the svn status of the current directory...

.. code-block:: bash

   $ svn status
    M      .
   X       castle
   X       pawn

...shows the properties of the existing directory have been modified and pawn is an external.
The directory must be committed to keep the change to 3.0.0 of pawn.
