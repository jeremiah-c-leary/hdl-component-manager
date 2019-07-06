Showing Components
==================

Use the **show** subcommand to view detailed information about a component.
This includes the component name, it's version, URL.
Optionally, every file that makes up the component can be listed along with it's md5sum.

Example:  Viewing information about rook
----------------------------------------

.. code-block:: bash

   $ hcm show bishop
   ----------     --------------------------------------------------------------------------
   Component      bishop                                                                    
   Version        1.1.0                                                                     
   URL            http://svn/my_repo/comps                                   
   Source         http://svn/my_repo/trunk/project_chess/components/bishop@26
   ----------     --------------------------------------------------------------------------

Example:  Viewing manifest
--------------------------

.. code-block:: bash

   $ hcm show rook --manifest
   ----------     ------------------------------------------------------------------------
   Component      rook                                                                    
   Version        3.0.0                                                                   
   URL            http://svn/my_repo/comps                                 
   Source         http://svn/my_repo/trunk/project_chess/components/rook@15
   ----------     ------------------------------------------------------------------------
   
   Manifest
   ---------------------------------------------------------
   10019aef04979acfac88673bc5dc6133    rook/lay/filelist.tcl
   a461fa565f1f7822bcdbda0b450df476    rook/rtl/rook.vhd

.. NOTE:: The manifest is extracted from the hcm.json file.
          It does not include any local changes to the files.
          Use the **validate** subcommand to compare the manifest against what is installed.

Example:  Viewing available upgrades
------------------------------------

All available upgrades and their log entries can be listed.

.. code-block:: bash

   $ hcm show rook --upgrades
   ------------     ------------------------------------------------------------------------
   Component        rook                                                                    
   Version          3.0.0                                                                   
   URL              http://svn/my_repo/comps                                 
   Source           http://svn/my_repo/trunk/project_chess/components/rook@41
   Dependencies     king, queen                                                             
   ------------     ------------------------------------------------------------------------
   
   Available Upgrades
   ==================
   
   Version: 4.0.0
   ------------------------------------------------------------------------
   r42 | jeremiah | 2019-06-11 19:09:53 -0500 (Tue, 11 Jun 2019) | 1 line
   
    "testing dependencies"
   ------------------------------------------------------------------------
   
   Version: 3.0.5
   ------------------------------------------------------------------------
   r51 | jeremiah | 2019-06-13 19:37:16 -0500 (Thu, 13 Jun 2019) | 1 line
   
    "Updating hcm config to the latest version."
   ------------------------------------------------------------------------
   
   Version: 3.0.4
   ------------------------------------------------------------------------
   r49 | jeremiah | 2019-06-12 20:02:38 -0500 (Wed, 12 Jun 2019) | 1 line
   
    "Adding invalid component to test how HCM handles it."
   ------------------------------------------------------------------------
   
   Version: 3.0.3
   ------------------------------------------------------------------------
   r35 | jeremiah | 2019-05-30 22:00:03 -0500 (Thu, 30 May 2019) | 1 line
   
    "testing -m works"
   ------------------------------------------------------------------------
   
   Version: 3.0.2
   ------------------------------------------------------------------------
   r34 | jeremiah | 2019-05-30 21:58:38 -0500 (Thu, 30 May 2019) | 6 lines
   
   This is a test of using the -F argument when publishing.
   
   It should allow the use of a file instead of a single line for the commit message.
   
   
   
   ------------------------------------------------------------------------
   
   Version: 3.0.1
   ------------------------------------------------------------------------
   r33 | jeremiah | 2019-05-30 21:57:37 -0500 (Thu, 30 May 2019) | 6 lines
   
   This is a test of using the -F argument when publishing.
   
   It should allow the use of a file instead of a single line for the commit message.
   
   
   
   ------------------------------------------------------------------------

Example:  Viewing modifications
-------------------------------

Modifications made to a component after installation can be viewed.
The **--modifications** argument will display the log entries for every change since the last install.
Both committed and uncommitted modifications will be shown.

.. code-block:: bash

   $ hcm show rook --modifications
   ------------     ------------------------------------------------------------------------
   Component        rook                                                                    
   Version          4.0.0                                                                   
   URL              http://svn/my_repo/comps                                 
   Source           http://svn/my_repo/trunk/project_chess/components/rook@41
   Dependencies     king, queen                                                             
   ------------     ------------------------------------------------------------------------
   
   Uncommitted Modifications
   =========================
   A  +    rook
   ?       rook/rtl/movement.vhd
   M  +    rook/rtl/rook-rtl.vhd
   
   Committed Modifications
   =======================
   ------------------------------------------------------------------------
   r63 | jeremiah | 2019-06-21 06:13:40 -0500 (Fri, 21 Jun 2019) | 2 lines
   
   Minor change to rook entity.
   
   ------------------------------------------------------------------------
   r62 | jeremiah | 2019-06-21 06:05:24 -0500 (Fri, 21 Jun 2019) | 2 lines
   
   Adding architecture.
   
   ------------------------------------------------------------------------

HCM will also indicate if no modifications were detected.

.. code-block:: bash

   $ hcm show rook --modifications
   ------------     ------------------------------------------------------------------------
   Component        rook                                                                    
   Version          4.0.0                                                                   
   URL              http://svn/my_repo/comps                                 
   Source           http://svn/my_repo/trunk/project_chess/components/rook@41
   Dependencies     king, queen                                                             
   ------------     ------------------------------------------------------------------------
   
   Uncommitted Modifications
   =========================
   No Uncommitted Modifications
   
   Committed Modifications
   =======================
   No Committed Modifications

