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

Example:  listing versions of a component
-----------------------------------------

Adding a component name to the end of the command will list all the versions and their log entries.

.. code-block:: bash

   $ hcm browse rook
   rook versions available:

   Version: 3.0.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.6.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.5.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.4.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.3.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.2.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.1.0
   ------------------------------------------------------------------------
   r59 | jeremiah | 2019-06-16 08:26:14 -0500 (Sun, 16 Jun 2019) | 2 lines
   
   Updating hcm.json files to correct format.
   
   ------------------------------------------------------------------------
   
   Version: 1.0.0
   ------------------------------------------------------------------------
   r10 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line
   
   initial release
   ------------------------------------------------------------------------



