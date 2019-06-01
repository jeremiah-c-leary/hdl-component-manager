Listing Components
==================

Use the **list** subcommand to view information about installed components.

Example:  listing installed components
--------------------------------------

.. code-block:: bash

   $ hcm list

   Component     Version      Upgrade      URL                                           
   ---------     --------     --------     ----------------------------------------------
   bishop        1.0.0        1.1.0        http://svn/my_repo/comps       
   castle        1.0.0        None         http://svn/external_repo/blocks
   pawn          1.0.0        None         http://svn/external_repo/blocks
   queen         1.0.0        1.1.0        http://svn/my_repo/comps       
   rook          1.1.0        3.0.3        http://svn/my_repo/comps       

The upgrade column shows the latest published version available.
There may be several versions between what is installed and what is available.
Use a repository browswer to determine if an upgrade is desired.
