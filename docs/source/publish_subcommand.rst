Publishing Components
=====================

Use the **publish** subcommand to add or update components in a repository.

There are a couple of requirements before a component can be published.

#.  component directory must be checked into SVN
#.  component directory must be status clean
#.  **HCM_URL_PATHS** should be defined

HCM uses **svn copy** commands to publish components.
This ensures a history is maintained for the component development.

Example:  Publishing a new component
------------------------------------

A new component can be published, but HCM must be told where to publish the component.
This can be done by setting the **HCM_URL_PATHS** environment variable or using the *--url* command line argument.
If only one path is defined in **HCM_URL_PATHS**, then HCM will use it as the publish location.
Using the *--url* command line argument will override **HCM_URL_PATHS**.

.. NOTE:: Publishing is restricted to the current repository.

.. code-block:: bash

   $ hcm publish bishop 1.0.0 --url http://svn/acme/chess/components -m "Initial release of bishop."

   INFO:Publishing component bishop as version 1.0.0
   INFO:Validating all files for component bishop are committed.
   INFO:Validating component exists in component directory...
   INFO:Creating component in component directory.
   INFO:Searching for hcm.json file...
   WARNING:Did not find hcm.json for component bishop.
   INFO:Creating default hcm.json file...
   INFO:Updating version...
   INFO:Updating source URL...
   INFO:Creating manifest...
   INFO:Writing configuration file bishop/hcm.json
   INFO:Adding configuration file to component directory
   INFO:Component published

HCM will create a configuration file named **hcm.json**.
This file contains information related to the component.

After publishing the component, use the **install** subcommand to switch the local component to the published version.

Example:  Publishing an update to a component
---------------------------------------------

If a component has been updated, the updates can be published.
Since the **hcm.json** file exists, the *--url* argument is not required.
HCM will use the information in the **hcm.json** file to determine where the component will be published.

.. code-block:: bash

   $ hcm publish bishop 1.1.0 -m "Fixing movement bug."

   INFO:Publishing component bishop as version 1.1.0
   INFO:Validating all files for component bishop are committed.
   INFO:Searching for hcm.json file...
   INFO:Validating component exists in component directory...
   INFO:Updating version...
   INFO:Updating source URL...
   INFO:Creating manifest...
   INFO:Writing configuration file bishop/hcm.json
   INFO:Adding configuration file to component directory
   INFO:Component published

HCM will update the **hcm.json** file with the new version before it is committed to the component directory.

After publishing the component, use the **install** subcommand to switch the local component to the published version.

Example:  Using a file for the commit message
---------------------------------------------

Publishing supports using a file for the commit message.
This is used instead of the *-m* command line option

.. code-block:: bash

   $ hcm publish bishop 1.1.0 -F release_notes.txt

   INFO:Publishing component bishop as version 1.1.0
   INFO:Validating all files for component bishop are committed.
   INFO:Searching for hcm.json file...
   INFO:Validating component exists in component directory...
   INFO:Updating version...
   INFO:Updating source URL...
   INFO:Creating manifest...
   INFO:Writing configuration file bishop/hcm.json
   INFO:Adding configuration file to component directory
   INFO:Component published

