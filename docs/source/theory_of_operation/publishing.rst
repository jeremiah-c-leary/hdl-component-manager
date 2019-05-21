Publishing
----------

Publishing uses the svn copy command to take snapshots of a component.
The command can only work within a repository.

In the diagram above, you can see all the publish actions take place between a repository and it's respective working copy.

To publish within the same repo:

1.  Ensure all files in a component to be published directory are committed.

    a.  Any unversioned files must be deleted
    b.  it must come back with a clean status

2.  generate the hcm.json or hcm.yaml file
3.  Add/Modify hcm.json file to the component directory
4.  svn copy the local component directory to the published directory under the correct version

