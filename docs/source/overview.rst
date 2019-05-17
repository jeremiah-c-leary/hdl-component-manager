Overview
========

HDL Component Manager (HCM) is a tool to manage IP blocks in an SVN repository.

It follows a particular method for managing IP blocks.
This method assumes all external IP is committed to your repo.
Following this method ensures you will always have access to code for you project.

Component Directory Structure
-----------------------------

The directory structure contains individual directories for each component.
This top level directory can be anywhere in your repository.
It is typically placed either at the root or under the tags directory.

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


Publishing Components
---------------------

Publishing is the act of saving a version of a component to the components directory.
This is typically done using an svn copy command.
The source of the copy can be either your working copy or another location in the repository.

.. code-block:: bash

  > hcm publish I2C_CONTROL 2.1.0



Pulling in Components
---------------------

Once components have been published you can pull versions into your local project location.
A YAML file controls which version of the component you bring in.

.. code-block:: yaml

  hcm:
      url : http://svn/program/tags/components
      components :
          I2C_CONTROL : version : 1.1.0
          SPI_CONTROL : version : 2.1.0
          External_Interfaces/SPI/4_wire : version : 1.1.0
 
In the above example, if you wanted to update to version 2.0.0 of the I2C_CONTROL component just change the YAML file and run update:

.. code-block:: yaml

  hcm:
      url : http://svn/program/tags/components
      components :
          I2C_CONTROL : version : 2.0.0
          SPI_CONTROL : version : 2.1.0
          External_Interfaces/SPI/4_wire : version : 1.1.0
 
.. code-block:: bash

    > hcm update

HCM will read all YAML files in the directory where it is executed.
It will combine all information under the 'hcm' key.
This allows you to divide your component configurations into smaller logical pieces.

