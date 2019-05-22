HCM configuration file
----------------------

The HCM configuration file is a JSON file which contains information about the component.
There is an HCM configuration file for each component and is updated with every version released.

.. code-block:: json

   {
     "hcm" : {
         "url" : "http://svn/my_repo/components",
         "name" : "rook",
         "source_url" : "http://svn/my_repo/chess_project/components/rook@1276",
         "version" : "1.0.0",
         "manifest" : {
             "rook/rtl/rook.vhd" : "93ffadcc3b73c6292de35564192a99b4",
             "rook/lay/filelist.tcl" : "10019aef04979acfac88673bc5dc6133"
         }
      }
    }

The JSON file starts with a single hash key named **hcm**.
This uniquely identifies the information as belonging to HCM.
It contains five other keys: url, name, version, source_url, and manifest.

The **url** key is the location of the component directory where this component has been published.

The **name** key is the name of the component.

The **source_url** key is the current URL path and revision where the component was published from.
This allows us to know the pedigree of the component across multiple repos.

The **version** key indicates the version of the component that has been published.

The **manifest** key holds a key value pair of every file that makes up the component.
The key is the name of the file relative.
The value is an md5sum hash of that file.

The manifest provides a quick method to validate any component to see if anything has changed.
It will also assist in transferring components between repos.

