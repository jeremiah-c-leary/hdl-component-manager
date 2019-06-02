
import logging
import os
import subprocess
import json

import hcm.svn as svn
import hcm.utils as utils


def extract_url(sUrl):

    if sUrl:
        return sUrl

    try:
        sHcmUrlPaths = os.environ['HCM_URL_PATHS']
    except KeyError:
        return None

    if sHcmUrlPaths.count(':') > 1:
        logging.error('Multiple HCM URL paths detected.')
        for sString in sHcmUrlPaths.split(','):
            logging.info('-- ' + sString)
        logging.error('Unable to determine correct path to component directory.')
        logging.info('Use the --url command line option to specify correct URL.')
        exit()

    return sHcmUrlPaths


def read_hcm_json_file(sComponentName):
    logging.info('Searching for hcm.json file...')
    sHcmName = sComponentName + '/hcm.json'
    try:
        with open(sHcmName) as json_file:
            return json.load(json_file)
    except IOError:
        logging.warning('Did not find hcm.json for component ' + sComponentName + '.')
        return None
    except ValueError:
        logging.warning('Error in JSON file ' + sComponentName + '/hcm.json')
        return None


def create_default_hcm_dictionary(sName, sVersion, sUrl):
    logging.info('Creating default hcm.json file...')
    dReturn = {}
    dReturn['hcm'] = {}
    dReturn['hcm']['url'] = sUrl
    dReturn['hcm']['source_url'] = ''
    dReturn['hcm']['name'] = sName
    dReturn['hcm']['version'] = sVersion
    dReturn['hcm']['manifest'] = {}
    return dReturn


def search_for_source_url(sLine, sSourceUrl, fSourceUrlFound):
    if sLine.startswith('URL:') and not fSourceUrlFound:
        sSourceUrl = sLine.split()[1]
        fSourceUrlFound = True
    return sSourceUrl, fSourceUrlFound


def search_for_maximum_revision(sLine, iMaxRevision):
    if sLine.startswith('Last Changed Rev:'):
        iMaxRevision = max(iMaxRevision, int(sLine.split()[-1]))
    return iMaxRevision


def update_source_url(dHcmConfig):
    logging.info('Updating source URL...')
    lOutput = svn.issue_command(['svn', 'info', '-R', dHcmConfig['hcm']['name']]).split('\n')
    fSourceUrlFound = False
    iMaxRevision = 0
    sSourceUrl = None
    for sLine in lOutput:
        sSourceUrl, fSourceUrlFound = search_for_source_url(sLine, sSourceUrl, fSourceUrlFound)
        iMaxRevision = search_for_maximum_revision(sLine, iMaxRevision)
    sSourceUrl += '@' + str(iMaxRevision)
    dHcmConfig['hcm']['source_url'] = sSourceUrl


def update_manifest(dHcmConfig):
    logging.info('Creating manifest...')
    dHcmConfig['hcm']['manifest'] = {}
    for root, dirs, files in os.walk(dHcmConfig['hcm']['name'], topdown=True):
        for name in files:
            sFileName = os.path.join(root, name)
            add_file_to_manifest(dHcmConfig, sFileName)


def add_file_to_manifest(dHcmConfig, sFileName):
    if 'hcm.json' in sFileName:
        return False
    if '.svn' in sFileName:
        return False
    dHcmConfig['hcm']['manifest'][sFileName] = calculate_md5sum(sFileName)
    return True


def calculate_md5sum(sFileName):
    lOutput = subprocess.check_output(['md5sum', sFileName], stderr=subprocess.STDOUT).decode('ascii').split('\n')
    return lOutput[0].split()[0]


def update_version(dHcmConfig, sVersion):
    logging.info('Updating version...')
    dHcmConfig['hcm']['version'] = sVersion


def write_configuration_file(dHcmConfig):
    sHcmConfigPath = utils.get_hcm_config_path(dHcmConfig)
    logging.info('Writing configuration file ' + sHcmConfigPath)
    with open(sHcmConfigPath, 'w') as outfile:
        json.dump(dHcmConfig, outfile, indent=4, sort_keys=True)


def add_hcm_config_file_to_component_directory(dHcmConfig):
    logging.info('Adding configuration file to component directory')
    try:
        return svn.issue_command(['svn', 'add', utils.get_hcm_config_path(dHcmConfig)])
    except subprocess.CalledProcessError:
        # File is already added
        pass


def copy_component_to_component_directory(dHcmConfig, oCommandLineArguments):
    sComponentName = utils.get_component_name(dHcmConfig)
    sUrl = utils.get_version_path(dHcmConfig)
    if oCommandLineArguments.f is None:
        svn.issue_command(['svn', 'cp', sComponentName, sUrl, '-m "' + oCommandLineArguments.m + '"'])
    else:
        svn.issue_command(['svn', 'cp', sComponentName, sUrl, '-F', oCommandLineArguments.f])

    logging.info('Component published')


def create_component_directory(sUrl):
    logging.info('Validating component exists in component directory...')
    if not svn.does_directory_exist(sUrl):
        logging.info('Creating component in component directory.')
        try:
            svn.mkdir(sUrl)
        except subprocess.CalledProcessError:
            logging.error('Could not create directory ' + sUrl)
            exit()


def check_if_version_already_exists(dHcmConfig):
    if svn.does_directory_exist(utils.get_version_path(dHcmConfig)):
        logging.error('Version ' + utils.get_version(dHcmConfig) + ' already exists')
        exit()
    return False


def does_component_directory_exist(sComponent):
    if not os.path.isdir(sComponent):
        logging.error('Component directory ' + sComponent + ' does not exist.')
        exit()
    return True


def publish(oCommandLineArguments):

        logging.info('Publishing component ' + oCommandLineArguments.component + ' as version ' + oCommandLineArguments.version)

        does_component_directory_exist(oCommandLineArguments.component)

        svn.is_directory_status_clean(oCommandLineArguments.component)

        sUrl = extract_url(oCommandLineArguments.url)

        dHcmConfig = read_hcm_json_file(oCommandLineArguments.component)
        if not dHcmConfig:
            dHcmConfig = create_default_hcm_dictionary(oCommandLineArguments.component, oCommandLineArguments.version, sUrl)

        create_component_directory(utils.get_component_path(dHcmConfig))
        update_version(dHcmConfig, oCommandLineArguments.version)
        check_if_version_already_exists(dHcmConfig)

        update_source_url(dHcmConfig)
        update_manifest(dHcmConfig)

        write_configuration_file(dHcmConfig)
        add_hcm_config_file_to_component_directory(dHcmConfig)
        copy_component_to_component_directory(dHcmConfig, oCommandLineArguments)
