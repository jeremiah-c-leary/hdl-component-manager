Overview
========

HDL Component Manager (HCM) is a tool to manage Hardware Description Language (HDL) IP blocks in an SVN repository.
It simplifies the sharing of hdl components between projects without having to perform merges.

With HCM you can:

#. Add new components
#. Switch between versions components
#. Publish updates to existing components
#. Track pedigree of components
#. Manage multiple versions of components

Why HCM?
--------

HCM was created after attempting to share components between two programs.
A merge was attempted from one program to another, and it did not go cleanly.
There were multiple instances where I thought a merge was successful, only to find out it was not.

I noticed support for packaging of HDL code lags software implementations.
Software has many package managers, e.g. PIP, APT, RPM, and YUM.
HCM is an attempt to provide similar capabilities of those package managers for HDL development.


Key Benefits
------------

* Provides a method to control versions of IP
* Controls the distribution of HDL code
* Can be used to control vendor IP

Key Features
------------

* Follows the Major.Minor.Patch method of version control
* Works with SVN repositories
* Automates publishing of code to a central location
* Automates installing and upgrading of code
* Supports multiple repositories
* Supports externals
* Language independent (VHDL, Verilog, System Verilog)
