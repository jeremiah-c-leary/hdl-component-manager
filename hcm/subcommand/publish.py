
import logging
import os
import subprocess
import json

import svn


def extract_url(oCommandLineArguments):

    if oCommandLineArguments.url:
        return oCommandLineArguments.url

    try:
        sHcmUrlPaths = os.environ['HCM_URL_PATHS']
    except KeyError:
        return None

    if sHcmUrlPaths.count(':') > 1:
        logging.error('Multiple HCM url paths detected.')
        for sString in sHcmUrlPaths.split(','):
            logging.info('-- ' + sString)
        logging.error('Unable to determine correct path to component directory.')
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


def create_default_hcm_dictionary(oCommandLineArguments, sUrl):
    logging.info('Creating default hcm.json file...')
    dReturn = {}
    dReturn['hcm'] = {}
    dReturn['hcm']['url'] = sUrl
    dReturn['hcm']['source_url'] = ''
    dReturn['hcm']['name'] = oCommandLineArguments.component
    dReturn['hcm']['version'] = oCommandLineArguments.version
    dReturn['hcm']['manifest'] = {}
    return dReturn


def update_source_url(dHcmConfig):
    logging.info('Updating source URL...')
    lOutput = subprocess.check_output(['svn', 'info', '-R', dHcmConfig['hcm']['name']], stderr=subprocess.STDOUT).split('\n')
    fSourceUrlFound = False
    iMaxRevision = 0
    for sLine in lOutput:
        if sLine.startswith('URL:') and not fSourceUrlFound:
            sSourceUrl = sLine.split()[1]
            fSourceUrlFound = True
        if sLine.startswith('Last Changed Rev:'):
            iMaxRevision = max(iMaxRevision, int(sLine.split()[-1]))
    sSourceUrl += '@' + str(iMaxRevision)
    dHcmConfig['hcm']['source_url'] = sSourceUrl


def update_manifest(dHcmConfig):
    logging.info('Creating manifest...')
    dHcmConfig['hcm']['manifest'] = {}
    for root, dirs, files in os.walk(dHcmConfig['hcm']['name'], topdown=True):
        for name in files:
            sFileName = os.path.join(root, name)
            if sFileName.startswith(dHcmConfig['hcm']['name'] + '/hcm.json'):
                continue
            dHcmConfig['hcm']['manifest'][sFileName] = calculate_md5sum(sFileName)
            calculate_md5sum(sFileName)


def update_version(dHcmConfig, sVersion):
    logging.info('Updating version...')
    dHcmConfig['hcm']['version'] = sVersion


def calculate_md5sum(sFileName):
    lOutput = subprocess.check_output(['md5sum', sFileName], stderr=subprocess.STDOUT).split('\n')
    return lOutput[0].split()[0]


def write_configuration_file(dHcmConfig):
    logging.info('Writing configuration file ' + dHcmConfig['hcm']['name'] + '/hcm.json')
    with open(dHcmConfig['hcm']['name'] + '/hcm.json', 'w') as outfile:
        json.dump(dHcmConfig, outfile, indent=4, sort_keys=True)


def add_hcm_config_file_to_component_directory(dHcmConfig):
    logging.info('Adding configuration file to component directory')
    try:
        lOutput = subprocess.check_output(['svn', 'add', dHcmConfig['hcm']['name'] + '/hcm.json'], stderr=subprocess.STDOUT).split('\n')
    except subprocess.CalledProcessError:
        # File is already added
        pass


def copy_component_to_component_directory(dHcmConfig, oCommandLineArguments):
    sComponentName = dHcmConfig['hcm']['name']
    sUrl = dHcmConfig['hcm']['url'] + '/' + sComponentName + '/' + dHcmConfig['hcm']['version']
    lOutput = subprocess.check_output(['svn', 'cp', sComponentName, sUrl, '-m "' + oCommandLineArguments.m + '"'], stderr=subprocess.STDOUT).split('\n')
    logging.info('Component published')


def check_svn_status_is_clean(sDirectory):
    logging.info('Validating all files for component ' + sDirectory + ' are committed.')
    lOutput = subprocess.check_output(['svn', 'status', sDirectory]).split('\n')[:-1]
    if len(lOutput) > 0:
        logging.error('The following files must be committed or removed:')
        for sOutput in lOutput:
            print(sOutput)
        exit()


def create_component_directory(sUrl):
    logging.info('Validating component exists in component directory...')
    if not svn.does_directory_exist(sUrl):
        logging.info('Creating component in component directory.')
        try:
            svn.mkdir(sUrl)
        except subprocess.CalledProcessError:
            logging.error('Could not create directory ' + sUrl)
            exit()


def publish(oCommandLineArguments):

        logging.info('Publishing component ' + oCommandLineArguments.component + ' as version ' + oCommandLineArguments.version)

        check_svn_status_is_clean(oCommandLineArguments.component)

        sUrl = extract_url(oCommandLineArguments)

        create_component_directory(sUrl + '/' + oCommandLineArguments.component)

        dHcmConfig = read_hcm_json_file(oCommandLineArguments.component)
        if not dHcmConfig:
            dHcmConfig = create_default_hcm_dictionary(oCommandLineArguments, sUrl)

        update_version(dHcmConfig, oCommandLineArguments.version)
        update_source_url(dHcmConfig)
        update_manifest(dHcmConfig)
  
        write_configuration_file(dHcmConfig)
        add_hcm_config_file_to_component_directory(dHcmConfig)
        copy_component_to_component_directory(dHcmConfig, oCommandLineArguments)



#        if does_svn_directory_exist(sUrl):
#            logging.error('Component directory ' + sUrl + ' already exists')
#            exit()
#        try:
#            svn_mkdir(sUrl)
#            logging.info('Add "' + sUrl + '" to the HCM_URL_PATHS environment variable.')
#        except subprocess.CalledProcessError:
#            logging.error('Could not create component directory ' + sUrl)
#            logging.error('Validate base URL path to repository is correct.')
#            exit()
