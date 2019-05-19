Theory of Operation
===================

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

