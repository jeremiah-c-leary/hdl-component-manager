
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
