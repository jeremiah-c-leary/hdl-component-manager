
def extract_hcm_json_revision(lOutput):
    fHcmDetected = False
    for sLine in lOutput:
        fHcmDetected = search_for_hcm_json_file(sLine, fHcmDetected)

        if 'Last Changed Rev:' in sLine and fHcmDetected:
            lLine = sLine.split()
            sHcmRevision = lLine[-1]
            return sHcmRevision
    return None


def search_for_hcm_json_file(sLine, fHcmDetected):
    if 'hcm.json' in sLine and not fHcmDetected:
        return True
    return fHcmDetected
