Create Component Directory
==========================

HCM will create the component directory and place it in an existing SVN repository.
This top level directory can be anywhere.
It is commonly placed either at the root or under the tags directory.

Creating a component directory
------------------------------

Use the **create** subcommand to create the reposistory location:

.. code-block:: bash

  $ hcm create <url>

Where *<url>* is the path to the component directory:

.. code-block:: bash

  $ hcm create http://svn/acme/project1/components
  INFO:Creating component directory http://svn/acme/project1/components
  INFO:Add "http://svn/acme/project1/components" to the HCM_URL_PATHS environment variable.

HCM will create any level of hierarchy necessary to create the given URL path.

HCM supports multiple component repos and can install/publish from/to any of them.

.. WARNING:: If the URL already exists, an error will be reported

You should update the **HCM_URL_PATHS** environment variable to point to the URL path just created.

.. code-block:: bash

  $ export HCM_URL_PATHS=http://svn/acme/components,$HCM_URL_PATHS

.. NOTE:: The separator is a comma and not a colon.
