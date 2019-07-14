
import logging

import hcm.svn as svn
import hcm.utils as utils


def download(oCommandLineArguments):

    download_component(oCommandLineArguments)

    logging.info('Download complete')


def download_component(oCommandLineArguments):
    sComponent = oCommandLineArguments.component
    sVersion = oCommandLineArguments.version

    logging.info('Downloading component ' + sComponent + ' version ' + sVersion)

    lUrl = utils.determine_url()

    sFinalUrlPath = utils.validate_urls(lUrl, sComponent, sVersion)

    svn.export(sFinalUrlPath, sComponent + '_' + sVersion)
