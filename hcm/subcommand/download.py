
import logging

import hcm.svn as svn
import hcm.utils as utils


def download(oCommandLineArguments):

    download_component(oCommandLineArguments)

    logging.info('Download complete')


def download_component(oCommandLineArguments):
    sUrl = None
    sComponent = oCommandLineArguments.component
    sVersion = oCommandLineArguments.version

    logging.info('Downloading component ' + sComponent + ' version ' + sVersion)

    lUrl = determine_url(sUrl)

    sFinalUrlPath = validate_urls(lUrl, sComponent, sVersion)

    svn.export(sFinalUrlPath, sComponent + '_' + sVersion)


def build_url_path(sUrl, sComponent, sVersion):
    sReturn = sUrl + '/' + sComponent + '/'
    return sReturn + sVersion


def determine_url(sUrl):
    if sUrl:
        return [sUrl]

    lUrl = utils.get_url_from_environment_variable()

    if lUrl is None:
        logging.error('URL path to components has not been specified.')
        logging.error('Use the --url option or set the HCM_URL_PATHS environment variable.')
        exit()

    return lUrl


def validate_urls(lUrl, sComponent, sVersion):
    fUrlPathFound = False
    fMultipleFound = False

    for sUrl in lUrl:
        sUrlPath = build_url_path(sUrl, sComponent, sVersion)
        if svn.does_directory_exist(sUrlPath):
            fMultipleFound = fUrlPathFound
            fUrlPathFound = True
            sFinalUrlPath = sUrlPath

    if not fUrlPathFound:
        logging.error('Component ' + sComponent + ' could not be found in the following URLs:')
        for sUrl in lUrl:
            print(sUrl)
        exit()

    if fMultipleFound:
        logging.warning('Component ' + sComponent + ' was found in multiple locations.')
        logging.info('Specify url using the --url command line argument.')
        exit()

    return sFinalUrlPath
