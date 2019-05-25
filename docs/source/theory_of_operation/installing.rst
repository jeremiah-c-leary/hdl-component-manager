Installing
----------

Installing can take place from a local repo or a remote repo.
If an install is performed from a local repo, then the svn copy command will be used.
This provides history between what is installed and what has been published.

If an install is performed from a remote repo, then the svn export command will be used.
This pulls the component from the other repo and copies it into the working copy.
The files need to be added and then committed.
History is not lost in this case, but it is a little more difficult to follow.

Local Install
~~~~~~~~~~~~~

This is the workflow for a local install:

.. image:: img/install_local.svg

#.  Check if local component directory is svn status clean
#.  Delete component directory in working copy
#.  SVN copy component version directory from local repo

HCM will perform all these steps.

.. NOTE:: Committing the install is left to the user.

Remote Install
~~~~~~~~~~~~~~

This is the workflow for a remote install:

.. image:: img/install_remote.svg

#.  Check if local component directory is svn status clean
#.  Delete component directory in working copy
#.  Export component from external repo
#.  Add exported component to working copy

HCM will perform all these steps.

.. NOTE:: Committing the install is left to the user.