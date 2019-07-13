Pushing
-------

Pushing is similar to publishing, but the with a slight nuance.
The goal of pushing is to replace the existing published component with a new copy.
This can be helpful if you want to control a rapidly evolving component without publishing versions.

The version for pushing can not follow the Major.Minor.Patch format.

.. NOTE:: HCM will not allow a component versioned with Major.Minor.Patch to be pushed.

To push manually you would follow these steps:

.. image:: img/push.svg

1.  Ensure requested component directory exists

2.  Validate all files in a component to be pushed are committed.

    a.  Any unversioned files must be deleted
    b.  it must come back with a clean status

3.  Lock component component directory

4.  Check out component version directory to temporary directory

5.  Delete everything under the checked directory except the .svn folder

6.  Copy everything under the directory to be pushed under the checked out directory

7.  Perform svn status and svn add everything that is a ?

8.  Perform svn status and svn delete everything that is a !

9.  Generate the hcm.json file if it does not exist

    a.  Read hcm.json file it is does exist
    b.  Update version and manifest fields

10.  Add hcm.json file to the component directory

11.  Commit changes in checked out directory

12.  Remove lock

13.  Delete temporary folder

HCM will validate step 2 has been completed before performing steps 3 through 6.

.. NOTE:: The hcm.json file has either been created or modified.
   HCM does not commit the file to the local component directory.
