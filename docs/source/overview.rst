Overview
========

HDL Component Manager (HCM) is a tool to manage Hardware Description Language (HDL) IP blocks in an SVN repository.
It simplifies the sharing of hdl components between projects without having to perform merges.

With HCM you can:

#. Add new components
#. Switch between versions components
#. Publish updates to existing components

Why HCM?
--------

Support for packaging of HDL code lags software implementations.
Software has many package managers, e.g. PIP, APT, RPM, and YUM.
HCM is an attempt to provide similar capabilities of those package managers for HDL development.

Key Benefits
------------

* Provides a method to control versions of IP
* Controls the distribution of HDL code
* Follows the Major.Minor.Patch method of version control
* Language independent (VHDL, Verilog, System Verilog)
* Can be used to control vendor IP

Key Features
------------

* Works with SVN repositories
* Automates publishing of code to a central location
* Automates installing and upgrading of code
* Supports multiple repositories
* Supports externals
