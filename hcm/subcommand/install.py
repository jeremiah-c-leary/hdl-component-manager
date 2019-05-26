
import logging

import hcm.svn as svn


def install(sUrl, sComponent, sVersion):

        logging.info('Installing component ' + sComponent + ' version ' + sVersion)

        sUrlPath = build_url_path(sUrl, sComponent, sVersion)

        if not svn.does_directory_exist(sUrlPath):
            logging.error('Could not find the following URL path to component: ' + sUrlPath)
            exit()

        svn.is_directory_status_clean(sComponent)

        svn.delete(sComponent)

        svn.copy(sUrlPath, sComponent)


def build_url_path(sUrl, sComponent, sVersion):
    return sUrl + '/' + sComponent + '/' + sVersion
