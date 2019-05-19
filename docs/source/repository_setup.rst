Repository Setup
================

HCM can create the component directory structure and place it in your repository.
This top level directory can be anywhere.
The directory structure contains individual directories for each component.
It is commonly placed either at the root or under the tags directory.

Component Directory Structure
-----------------------------

Under each component directory are releases.
Each release follows the form of a three dot number: <Major>.<Minor>.<Patch>

.. code-block:: bash

   components
   |
   +-- I2C_CONTROL
   |   |
   |   +-- 1.0.0
   |   +-- 1.1.0
   |   +-- 2.0.0
   |
   +-- SPI_MASTER_CONTROL
   |   |
   |   +-- 1.0.0
   |   +-- 2.0.0
   |   +-- 2.1.0
   |   +-- 3.0.0
   |
   +-- SPI_SLAVE_CONTROL
       |
       +-- 1.0.0
       +-- 2.0.0
       +-- 2.1.0
       +-- 3.0.0

This allows you to organize the IP into folders instead of having every component at the same level.

Creating a component repo
-------------------------

Use the **create** subcommand to create the reposistory location:

.. code-block:: bash

  $ hcm create repo <url>

Where *<url>* is the path to the component directory:

.. code-block:: bash

  $ hcm create repo http://svn/acme/project1/components
  $ hcm create repo http://svn/acme/project2/components
  $ hcm create repo http://svn/acme/components

HCM will create any level of hierarchy necessary to create the given URL path.

HCM supports multiple component repos and can pull and publish to/from any of them.

.. WARNING:: If the URL already exists, an error will be reported

You will need to update the **HCM_PATHS** environment variable to point to the URL path just created.

.. code-block:: bash

  $ export HCM_URL_PATHS=http://svn/acme/components:$HCM_URL_PATHS

