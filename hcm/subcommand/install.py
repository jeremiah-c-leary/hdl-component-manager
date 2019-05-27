
import logging

import hcm.svn as svn
import hcm.utils as utils


def install(sUrl, sComponent, sVersion):

        logging.info('Installing component ' + sComponent + ' version ' + sVersion)

        sUrl = determine_url(sUrl)

        sUrlPath = build_url_path(sUrl, sComponent, sVersion)

        if not svn.does_directory_exist(sUrlPath):
            logging.error('Could not find the following URL path to component: ' + sUrlPath)
            exit()

        svn.is_directory_status_clean(sComponent)

        logging.info('Removing local component directory')
        svn.delete(sComponent)

        svn.copy(sUrlPath, sComponent)
        logging.info('Installation complete')


def build_url_path(sUrl, sComponent, sVersion):
    return sUrl + '/' + sComponent + '/' + sVersion


def determine_url(sUrl):
    if sUrl:
        return sUrl

    lUrl = utils.get_url_from_environment_variable()

    if lUrl == None:
        logging.error('URL path to components has not been specified.')
        logging.error('Use the --url option or set the HCM_URL_PATHS environment variable.')
        exit()

    if len(lUrl) > 1:
        logging.error('Multiple paths specified in HCM_URL_PATHS.')
        logging.error('Use the --url option to specify URL.')
        exit()

    return lUrl[0]
