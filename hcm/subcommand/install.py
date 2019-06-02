
import logging
import os
import shutil

import hcm.svn as svn
import hcm.utils as utils


def install(oCommandLineArguments):

        sUrl = oCommandLineArguments.url
        sComponent = oCommandLineArguments.component
        sVersion = oCommandLineArguments.version
        fForce = oCommandLineArguments.force
        fExternal = oCommandLineArguments.external

        logging.info('Installing component ' + sComponent + ' version ' + sVersion)

        lUrl = determine_url(sUrl)

        sFinalUrlPath = validate_urls(lUrl, sComponent, sVersion)

        fExternalled = is_component_externalled(sComponent, fExternal)

        if not fForce:
            svn.is_directory_status_clean(sComponent)

        remove_local_component_directory(sComponent, fForce, fExternalled)

        sRootUrl = svn.extract_root_url_from_directory('.')
        if fExternalled:
            update_externals(sFinalUrlPath, sComponent)
            svn.issue_command(['svn', 'update', '.'])
        elif sFinalUrlPath.startswith(sRootUrl):
            svn.copy(sFinalUrlPath, sComponent)
        else:
            svn.export(sFinalUrlPath, sComponent)

        logging.info('Installation complete')


def remove_local_component_directory(sComponent, fForce, fExternalled):
        logging.info('Removing local component directory')
        if os.path.isdir(sComponent):
            if fExternalled:
                shutil.rmtree(sComponent, ignore_errors=True)
            else:
                svn.delete(sComponent, fForce)


def build_url_path(sUrl, sComponent, sVersion):
    return sUrl + '/' + sComponent + '/' + sVersion


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
        logging.error('Component ' + sComponent + ' could not be found.')
        exit()

    if fMultipleFound:
        logging.warning('Component ' + sComponent + ' was found in multiple locations.')
        logging.info('Specify url using the --url command line argument.')
        exit()

    return sFinalUrlPath


def is_component_externalled(sComponent, fExternal):
    if fExternal:
        return True

    lExternals = svn.get_externals('.').split('\n')[:-1]
    for sExternal in lExternals:
        if sExternal.endswith(sComponent):
            return True
    return False


def update_externals(sUrlPath, sComponent):
    logging.info('Updating externals')
    lExternals = svn.get_externals('.').split('\n')[:-1]
    lFile = []
    for sExternal in lExternals:
        if sExternal.endswith(sComponent):
            lFile.append(sUrlPath + ' ' + sComponent)
        else:
            lFile.append(sExternal)

    with open('.hcm_externals.txt', 'w') as outfile:
        for sLine in lFile:
            outfile.write(sLine + '\n')
    svn.issue_command(['svn', 'propset', 'svn:externals', '-F' '.hcm_externals.txt', '.'])
    os.remove('.hcm_externals.txt')
