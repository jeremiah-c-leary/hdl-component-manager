Publishing Components
=====================

Use the **publish** subcommand to add or update components in the component directory.

There are a couple of requirements before a component can be published.

#.  component directory must be checked into SVN
#.  component directory must be status clean
#.  **HCM_URL_PATHS** should be defined

HCM uses SVN copy commands to publish components.
This ensures a history is maintained for the component development.

If the **HCM_URL_PATHS** is defined, and there is a single 
If there is only one path defined in the **HCM_URL_PATHS** environment variable, then the *--url* argument is optional.
Otherwise HCM will indicate the *--url* argument is required, as it will not know which repo to store the component.

Example:  Publishing a new component
------------------------------------

A new component can be published, but HCM must be told where to publish the component.
This can be done by setting the **HCM_URL_PATHS** environment variable.
If only one path is defined, HCM will use it as the publish location.
There is also a *--url* command line argument that will tell HCM where to publish the component.
The argument will override any paths in the **HCM_URL_PATH**.

.. NOTE:: Publishing is restricted to the current repository.

.. code-block:: bash

   $ hcm publish temp_ctrl 1.0.0 --url http://svn/acme/project1/components -m "Initial release of temperature controller."

   [jcl - need some output]

HCM will create a configuration file named **hcm.json**.
This file will contain information related to the component.

After publishing the component, use the **install** subcommand to switch the local component to the published version.

Example:  Publishing an update to a component
---------------------------------------------

If a component has been updated, the updates can be published.
Since the **hcm.json** file exists, the *--url* argument is not required.
HCM will use the information in the **hcm.json** file to determine where the component will be published.

.. code-block:: bash

   $ hcm publish temp_ctrl 1.1.0 -m "Fixing bug..."

   [jcl - need some output]

HCM will update the **hcm.json** file with the new version before it is committed to the component directory.

After publishing the component, use the **install** subcommand to switch the local component to the published version.

hcm.json file
-------------

The hcm.json file looks like this:

.. code-block:: yaml

   {
     "hcm" : {
       "url" : "http://svn/acme/project1/components",
       "source_url" : :http://svn/acme/project1/trunk/components/temp_ctrl@2938",
       "name" : "temp_ctrl",
       "version" : "1.1.0",
       "manifest" : {
         "file1" : "<md5sum>",
         "file2" : "<md5sum>",
         "filen" : "<md5sum>"
       }
     }
   }

