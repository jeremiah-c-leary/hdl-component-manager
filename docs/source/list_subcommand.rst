Listing Components
==================

Use the **list** subcommand to view information about installed components.

Example:  listing installed components
--------------------------------------

.. code-block:: bash

   $ hcm list

   Component     Version      URL                                           
   ---------     --------     ----------------------------------------------
   bishop        1.1.0        http://svn/my_repo/comps       
   castle        1.0.0        http://svn/external_repo/blocks
   pawn          1.0.0        http://svn/external_repo/blocks
   rook          1.1.0        http://svn/my_repo/comps       

Example:  listing upgrades available
------------------------------------

.. code-block:: bash

   $ hcm list --upgrades

   [jcl - need some output]

.. WARNING::  This is not implemented yet.
