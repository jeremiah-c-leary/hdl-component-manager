Downloading Components
======================

Use the **download** subcommand to pull down a specific version of a component without installing it.
This can be useful when trying to merge two versions of a component.

Example:  Downloading a Component
---------------------------------

After viewing the component repository, we decide to download version 1.1.0 of the component rook.

.. code-block:: bash

   $ hcm download rook 1.1.0
   INFO:Downloading component rook version 1.1.0
   INFO:Download complete


HCM will use the paths in the **HCM_URL_PATHS** environment variable.
It will search each path for a matching component name and version.

