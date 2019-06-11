Listing Components
==================

Use the **list** subcommand to view information about installed components.

Example:  listing installed components
--------------------------------------

.. code-block:: bash

   $ hcm list

   Component     Version      Upgrade      Status     URL                                           
   ---------     --------     --------     ------     -------------------------------
   bishop        1.1.0        None           U        http://svn/my_repo/comps       
   castle        1.0.0        None         E U        http://svn/external_repo/blocks
   pawn          1.0.0        3.1.0        E U        http://svn/external_repo/blocks
   rook          3.0.0        3.0.3         MU        http://svn/my_repo/comps       


The upgrade column shows the latest published version available.
There may be several versions between what is installed and what is published.
Use a repository browser to decide whether to upgrade a component.


+---------------+------------------------------------------------------------------------------+
| Column        | Description                                                                  |
+===============+==============================================================================+
| Component     | The name of the component installed.                                         |
+---------------+------------------------------------------------------------------------------+
| Version       | The version of the installed component.                                      |
+---------------+------------------------------------------------------------------------------+
| Upgrade       | The latest published version of the component.                               |
+---------------+------------------------------------------------------------------------------+
| Status        | Flags indicating information about the component.                            |
|               |                                                                              |
|               | E = Component was installed as an external.                                  |
|               |                                                                              |
|               | M = Component has commited modifications.                                    |
|               |                                                                              |
|               | U = Component has uncommitted modifications                                  |
+---------------+------------------------------------------------------------------------------+
| URL           | The base URL the component was installed from.                               |
+---------------+------------------------------------------------------------------------------+
