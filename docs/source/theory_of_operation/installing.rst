Installing
----------

Installing can take place within a repo or between repos.
If an install is performed within a repo, then the svn copy command will be used.
This provides history between what is installed and what has been published.

If an install is performed from another repo, then the svn export command will be used.
This pulls the component from the other repo and copies it into the working copy.
The working copy then needs to add the code and commit it.
History is not lost in this case, but it is a little more difficult to follow.

Remote Install
~~~~~~~~~~~~~~

Interestingly, any install from a repo outside your own will have to be an export then commit:

1.  Delete component directory in working copy
2.  Export component from external repo
3.  Commit component

Local Install
~~~~~~~~~~~~~

This would be different from your own repo:

1.  Delete component directory in working copy
2.  SVN copy component from internal repo
3.  Commit component

