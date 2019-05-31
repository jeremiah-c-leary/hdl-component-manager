Installing Components
=====================

Use the **install** subcommand to bring in a new component that is not part of your current working copy.
The URL path to the component and the version are required to install a new component.
This can be found using a repository browser or the **svn ls** subcommand.

Example:  installing the rook component
---------------------------------------

After viewing the component repository, we decide to pull in version 3.0.0 of the rook component.

.. code-block:: bash

   $ hcm install rook 3.0.0
   INFO:Installing component rook version 3.0.0
   INFO:Validating all files for component rook are committed.
   INFO:Removing local component directory
   INFO:Installation complete

HCM will use the paths in the **HCM_URL_PATHS** environment variable and search for the component name.
HCM will then check if the version exists.

Example:  installing the rook component when files rook directory are not committed
-----------------------------------------------------------------------------------

If the status of files underneath the component directory are not svn clean, then HCM will not perform the installation.
This behavior can be overridden by using the **--force** command line option.

.. code-block:: bash

   $ hcm install rook 3.0.0 --force
   INFO:Installing component rook version 3.0.0
   INFO:Removing local component directory
   INFO:Installation complete

Example:  installing from an external repo
------------------------------------------

When installing from an external repo, HCM will use the **svn export** command instead of **svn copy**.

.. code-block:: bash

   $ hcm install pawn 1.0.0 --url http://svn/external_repo/blocks
   INFO:Installing component pawn version 1.0.0
   INFO:Validating all files for component pawn are committed.
   INFO:Removing local component directory
   INFO:Installation complete

   $ svn status
   ?       pawn

After performing the install, the directory must be added using the **svn add** command, and then committed.

.. code-block:: bash

   $ svn add pawn
   A         pawn
   A         pawn/hcm.json
   A         pawn/rtl
   A         pawn/rtl/pawn.vhd

   $ svn commit pawn

