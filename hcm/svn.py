
import subprocess
import logging


def issue_command(lCommand):
    try:
        return subprocess.check_output(lCommand, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise e


def does_directory_exist(sUrl):
    try:
        issue_command(['svn', 'list', sUrl])
        return True
    except subprocess.CalledProcessError:
        return False
    except TypeError:
        return False


def mkdir(sUrl):
    try:
        issue_command(['svn', 'mkdir', '--parents', sUrl, '-m HCM: Creating componet directory.'])
        return True
    except subprocess.CalledProcessError as e:
        raise e


def is_directory_status_clean(sDirectory):
    logging.info('Validating all files for component ' + sDirectory + ' are committed.')
    lOutput = issue_command(['svn', 'status', sDirectory]).split('\n')[:-1]
    if len(lOutput) > 0:
        logging.error('The following files must be committed or removed:')
        for sOutput in lOutput:
            print(sOutput)
        exit()
    return True


def delete(sDirectory, fForce=False):
    try:
        if fForce:
            return issue_command(['svn', 'delete', '--force', sDirectory])
        else:
            return issue_command(['svn', 'delete', sDirectory])
    except subprocess.CalledProcessError as e:
        raise e


def copy(sSource, sDestination):
    try:
        return issue_command(['svn', 'copy', sSource, sDestination])
    except subprocess.CalledProcessError as e:
        raise e


def extract_root_url_from_directory(sDirectory):
    try:
        lOutput = issue_command(['svn', 'info', sDirectory]).split('\n')
        for sLine in lOutput:
            if sLine.startswith('Repository Root:'):
                lLine = sLine.split()
                return lLine[-1]
    except subprocess.CalledProcessError as e:
        raise e


def export(sSource, sDestination):
    try:
        return issue_command(['svn', 'export', sSource, sDestination])
    except subprocess.CalledProcessError as e:
        raise e


def get_externals(sDirectory):
    try:
        return issue_command(['svn', 'propget', 'svn:externals', sDirectory])
    except subprocess.CalledProcessError:
        return None


def directory_has_committed_modifications(sDirectory):
    lOutput = issue_command(['svn', 'info', '-R', sDirectory]).split('\n')

    sHcmRevision = extract_hcm_json_revision(lOutput)

    if sHcmRevision is None:
        return False

    return is_there_a_file_with_a_later_revision_than_hcm_json(lOutput, sHcmRevision)


def is_there_a_file_with_a_later_revision_than_hcm_json(lOutput, sHcmRevision):
    sRevision = what_is_the_latest_file_revision(lOutput)
    if str(sRevision) != str(sHcmRevision):
        return True

    return False


def what_is_the_latest_file_revision(lOutput):
    iMaxRevision = 0
    for sLine in lOutput:
        if 'Revision' in sLine:
            lLine = sLine.split()
            iMaxRevision = max(iMaxRevision, int(lLine[-1]))
    return iMaxRevision


def extract_hcm_json_revision(lOutput):
    fHcmDetected = False
    for sLine in lOutput:
        if 'hcm.json' in sLine and not fHcmDetected:
            fHcmDetected = True
        if 'Revision' in sLine and fHcmDetected:
            lLine = sLine.split()
            sHcmRevision = lLine[-1]
            return sHcmRevision
    return None


def does_directory_have_uncommitted_files(sDirectory):
    lOutput = issue_command(['svn', 'status', sDirectory]).split('\n')[:-1]
    if len(lOutput) > 0:
        return True
    return False
