
import logging
import subprocess


def does_svn_directory_exist(sUrl):
    try:
        subprocess.check_output(['svn', 'list', sUrl], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def svn_mkdir(sUrl):
    try:
        subprocess.check_output(['svn', 'mkdir', '--parents', sUrl, '-m HCM: Creating componet directory.'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise e


def create(sUrl):

        logging.info('Creating component directory ' + sUrl)

        if does_svn_directory_exist(sUrl):
            logging.error('Component directory ' + sUrl + ' already exists')
            exit()
        try:
            svn_mkdir(sUrl)
            logging.info('Add "' + sUrl + '" to the HCM_URL_PATHS environment variable.')
        except subprocess.CalledProcessError:
            logging.error('Could not create component directory ' + sUrl)
            logging.error('Validate base URL path to repository is correct.')
            exit()
