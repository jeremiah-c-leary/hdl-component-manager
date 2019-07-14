
import logging
import os
import shutil

import hcm.svn as svn
import hcm.utils as utils


def install(oCommandLineArguments):

    install_component(oCommandLineArguments)

    if oCommandLineArguments.dependencies:
        lInstalledDependencies = [oCommandLineArguments.component]

        oCommandLineArguments.version = None
        logging.info('Installing dependencies')
        install_dependencies(oCommandLineArguments, lInstalledDependencies)

    logging.info('Installation complete')


def install_dependencies(oCommandLineArguments, lInstalledDependencies):

    lDependencies = get_dependencies(oCommandLineArguments.component)
    for sDependent in lDependencies:
        if sDependent in lInstalledDependencies:
            continue
        oCommandLineArguments.component = sDependent
        if os.path.isdir(sDependent) and not oCommandLineArguments.upgrade:
            logging.info('Component ' + sDependent + ' is already installed')
        else:
            install_component(oCommandLineArguments)
            lInstalledDependencies.append(sDependent)
            install_dependencies(oCommandLineArguments, lInstalledDependencies)


def get_dependencies(sComponent):
    logging.info('Checking for dependencies of ' + sComponent)

    dFileDependencies = utils.read_dependencies(sComponent)
    try:
        return dFileDependencies['requires'].keys()
    except TypeError:
        logging.info('  No Dependencies found')
        return []


def install_component(oCommandLineArguments):
    sUrl = oCommandLineArguments.url
    sComponent = oCommandLineArguments.component
    sVersion = oCommandLineArguments.version
    fForce = oCommandLineArguments.force
    fExternal = oCommandLineArguments.external

    if sVersion is None:
        logging.info('Installing component ' + sComponent)
    else:
        logging.info('Installing component ' + sComponent + ' version ' + sVersion)

    lUrl = utils.determine_url(sUrl)

    sFinalUrlPath = utils.validate_urls(lUrl, sComponent, sVersion)

    fExternalled = svn.is_component_externalled(sComponent, fExternal)

    if svn.is_directory_under_svn_control(sComponent) and fExternal and not svn.is_component_externalled(sComponent, False):
        logging.error('Can not install external over a committed directory.')
        logging.error('SVN delete component and commit first, then you can install an external.')
        exit()

    if not fForce:
        svn.is_directory_status_clean(sComponent)

    remove_local_component_directory(sComponent, fForce, fExternalled)

    sRootUrl = svn.extract_root_url_from_directory('.')
    if fExternalled:
        update_externals(sFinalUrlPath, sComponent)
        svn.update_current_directory()
    elif sFinalUrlPath.startswith(sRootUrl):
        svn.copy(sFinalUrlPath, sComponent)
    else:
        svn.export(sFinalUrlPath, sComponent)


def remove_local_component_directory(sComponent, fForce, fExternalled):
        logging.info('Removing local component directory')
        if os.path.isdir(sComponent):
            if fExternalled:
                shutil.rmtree(sComponent, ignore_errors=True)
            else:
                svn.delete(sComponent, fForce)


def update_externals(sUrlPath, sComponent):
    logging.info('Updating externals')
    lExternals = svn.get_externals('.').split('\n')[:-1]
    lFile = []
    fExternalFound = False
    for sExternal in lExternals:
        if sExternal == '':
            continue
        if sExternal.endswith(sComponent):
            lFile.append(sUrlPath + ' ' + sComponent)
            fExternalFound = True
        else:
            lFile.append(sExternal)

    if not fExternalFound:
        lFile.append(sUrlPath + ' ' + sComponent)

    with open('.hcm_externals.txt', 'w') as outfile:
        for sLine in lFile:
            if sLine is lFile[-1]:
                outfile.write(sLine)
            else:
                outfile.write(sLine + '\n')
    svn.issue_command(['svn', 'propset', 'svn:externals', '-F' '.hcm_externals.txt', '.'])
    os.remove('.hcm_externals.txt')
