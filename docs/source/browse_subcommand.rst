Browsing Components
===================

Use the **browse** subcommand to view information about components available for installation.

Example:  listing available components
--------------------------------------

.. code-block:: bash

   $ hcm browse

   Component     Version      URL                                           
   ---------     --------     -------------------------------
   bishop        1.1.0        http://svn/my_repo/comps       
   castle        1.0.0        http://svn/external_repo/blocks
   pawn          1.0.0        http://svn/external_repo/blocks
   rook          3.0.0        http://svn/my_repo/comps       


+---------------+------------------------------------------------------------------------------+
| Column        | Description                                                                  |
+===============+==============================================================================+
| Component     | The name of the component installed.                                         |
+---------------+------------------------------------------------------------------------------+
| Version       | The latest version available for the component.                              |
+---------------+------------------------------------------------------------------------------+
| URL           | The URL the component can be installed from.                                 |
+---------------+------------------------------------------------------------------------------+
