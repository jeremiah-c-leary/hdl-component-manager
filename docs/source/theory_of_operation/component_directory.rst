Component Directory Structure
-----------------------------

HCM can create the component directory structure and place it in your repository.
It is commonly placed either at the root of the repository or under the tags directory.

The component directory contains individual directories for each component.
Under each individual component name are the releases for that component.
Each release directory follows the form of a three dot number: <Major>.<Minor>.<Patch>

The example below shows a component directory with three components: rook, king, and queen.

The *rook* component has three releases: 1.0.0, 1.1.0, and 2.0.0.

The *king* component has four releases: 1.0.0, 2.0.0, 2.1.0, and 3.0.0.

The *queen* component has four releases: 1.0.0, 2.0.0, 2.1.0, and 3.0.0.

.. code-block:: bash

   components
   |
   +-- rook
   |   |
   |   +-- 1.0.0
   |   +-- 1.1.0
   |   +-- 2.0.0
   |
   +-- king
   |   |
   |   +-- 1.0.0
   |   +-- 2.0.0
   |   +-- 2.1.0
   |   +-- 3.0.0
   |
   +-- queen
       |
       +-- 1.0.0
       +-- 2.0.0
       +-- 2.1.0
       +-- 3.0.0

With this directory structure in the repository, differences between releases can be easily determined by comparing the two release URLs.
You also have a complete history of all the releases visible.
