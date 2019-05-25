
import logging
import subprocess

import hcm.svn as svn


def create(sUrl):

        logging.info('Creating component directory ' + sUrl)

        if svn.does_directory_exist(sUrl):
            logging.error('Component directory ' + sUrl + ' already exists')
            exit()
        try:
            svn.mkdir(sUrl)
            logging.info('Add "' + sUrl + '" to the HCM_URL_PATHS environment variable.')
            return True
        except subprocess.CalledProcessError:
            logging.error('Could not create component directory ' + sUrl)
            logging.error('Validate base URL path to repository is correct.')
            exit()
