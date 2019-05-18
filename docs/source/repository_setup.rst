Repository Setup
================

HCM can create the component directory structure and place it in your repository.
This top level directory can be anywhere.
The directory structure contains individual directories for each component.
It is typically placed either at the root or under the tags directory.

Component Directory Structure
-----------------------------

Under each component directory are releases in the form of a three dot number: <Major>.<Minor>.<Patch>

.. code-block:: bash

   components
   |
   +-- I2C_CONTROL
   |   |
   |   +-- 1.0.0
   |   +-- 1.1.0
   |   +-- 2.0.0
   |
   +-- SPI_CONTROL
       |
       +-- 1.0.0
       +-- 2.0.0
       +-- 2.1.0
       +-- 3.0.0

HCM supports a multiple level repository structure also:

.. code-block:: bash

   components
   |
   +-- SPI_CONTROL
       |
       +-- 3_wire
       |   +-- 1.0.0
       |   +-- 2.0.0
       |   +-- 3.0.0
       |
       +-- 4_wire
           +-- 1.0.0
           +-- 2.0.0
           +-- 2.1.0

This allows you to organize the IP into folders instead of having everying at the top level.

Creating a component repo
-------------------------

Use the **create** argument to create the reposistory location:

.. code-block:: bash

  $ hcm create repo <url>

Where *<url>* is the path to the component directory.
Examples:

.. code-block:: bash

  $ hcm create repo http://svn/acme/project1/components
  $ hcm create repo http://svn/acme/project2/components
  $ hcm create repo http://svn/acme/components

HCM supports multiple component repos and can pull from any of them.

.. NOTE:: 
    Publishing components not in your local repo requires manual effort.
    Hopefully this can be fixed as the program is developed.

.. NOTE:: If the URL already exists, an error will be reported
