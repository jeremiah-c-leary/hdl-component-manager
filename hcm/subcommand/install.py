
import logging
import os

import hcm.svn as svn
import hcm.utils as utils


def install(sUrl, sComponent, sVersion, fForce):

        logging.info('Installing component ' + sComponent + ' version ' + sVersion)

        lUrl = determine_url(sUrl)
        fUrlPathFound = False
        fMultipleFound = False

        for sUrl in lUrl:
            sUrlPath = build_url_path(sUrl, sComponent, sVersion)

            if svn.does_directory_exist(sUrlPath):
                if fUrlPathFound:
                    fMultipleFound = True
                fUrlPathFound = True
                sFinalUrlPath = sUrlPath

        if not fUrlPathFound:
            logging.error('Component ' + sComponent + ' could not be found.')
            exit()

        if fMultipleFound:
            logging.warning('Component ' + sComponent + ' was found in multiple locations.')
            logging.info('Specify url using the --url command line argument.')
            exit()

        if not fForce:
            svn.is_directory_status_clean(sComponent)

        logging.info('Removing local component directory')
        if os.path.isdir(sComponent):
            svn.delete(sComponent, fForce)

        sRootUrl = svn.extract_root_url_from_directory('.')
        if sFinalUrlPath.startswith(sRootUrl):
            svn.copy(sFinalUrlPath, sComponent)
        else:
            svn.export(sFinalUrlPath, sComponent)

        logging.info('Installation complete')


def build_url_path(sUrl, sComponent, sVersion):
    return sUrl + '/' + sComponent + '/' + sVersion


def determine_url(sUrl):
    if sUrl:
        return [sUrl]

    lUrl = utils.get_url_from_environment_variable()

    if lUrl == None:
        logging.error('URL path to components has not been specified.')
        logging.error('Use the --url option or set the HCM_URL_PATHS environment variable.')
        exit()

    return lUrl
