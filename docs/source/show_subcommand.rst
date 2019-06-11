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
