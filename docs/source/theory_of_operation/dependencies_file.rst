Dependencies file
-----------------

The HCM Dependencies file is a YAML file listing other components required.

.. code-block:: yaml

   ---
   requires:
      component1:
      component2:

      componentn:

Each *component* entry is a key that currently does not have a value.
This format was chosen to allow for easy extension of the dependency feature.

This file must be named **dependencies.yaml** and placed at the root of the component.
HCM will search for this file when installing to see if any other components must be installed.
