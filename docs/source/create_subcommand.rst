Create Component Directory
==========================

HCM will create the component directory and place it in an existing SVN repository.
This top level directory can be anywhere.
However, it is commonly placed either at the root or under the tags directory.

Creating a component directory
------------------------------

Use the **create** subcommand to create the component directory in a repository:

.. code-block:: bash

  $ hcm create http://svn/my_repo/components
  INFO:Creating component directory http://svn/my_repo/components
  INFO:Add "http://svn/my_repo/components" to the HCM_URL_PATHS environment variable.

HCM will create any level of hierarchy necessary to create the given URL path.

.. WARNING:: If the URL already exists, an error will be reported

Adding the URL to the **HCM_URL_PATHS** environment variable will give HCM visibility to those repositories.

.. code-block:: bash

  $ export HCM_URL_PATHS=http://svn/acme/components,$HCM_URL_PATHS

.. NOTE:: The separator is a comma and not a colon.
