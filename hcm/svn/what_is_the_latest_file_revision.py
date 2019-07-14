
def what_is_the_latest_file_revision(lOutput, sDirectory):
    iMaxRevision = 0
    fDirectoryFound = False
    for sLine in lOutput:
        if 'Last Changed Rev:' in sLine and not fDirectoryFound:
            fDirectoryFound = True
            continue
        iMaxRevision = get_maximum_revision(iMaxRevision, sLine)
    return iMaxRevision


def get_maximum_revision(iMaxRevision, sLine):
    if 'Last Changed Rev:' in sLine:
        lLine = sLine.split()
        iMaxRevision = max(iMaxRevision, int(lLine[-1]))
    return iMaxRevision
