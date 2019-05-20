
import logging
import os
import subprocess


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
    lOutput = subprocess.check_output(['svn', 'info', dHcmConfig['hcm']['name']], stderr=subprocess.STDOUT).split('\n')
    for sLine in lOutput:
        if sLine.startswith('URL:'):
            sSourceUrl = sLine.split()[1]
        if sLine.startswith('Last Changed Rev:'):
            sSourceUrl += '@' + sLine.split()[-1]
    dHcmConfig['hcm']['source_url'] = sSourceUrl


def update_manifest(dHcmConfig):
    logging.info('Creating manifest...')
    for root, dirs, files in os.walk(dHcmConfig['hcm']['name'], topdown=True):
        for name in files:
            sFileName = os.path.join(root, name)
            dHcmConfig['hcm']['manifest'][sFileName] = calculate_md5sum(sFileName)
            calculate_md5sum(sFileName)


def calculate_md5sum(sFileName):
    lOutput = subprocess.check_output(['md5sum', sFileName], stderr=subprocess.STDOUT).split('\n')
    return lOutput[0].split()[0]
    

def publish(oCommandLineArguments):

        logging.info('Publishing component ' + oCommandLineArguments.component + ' as version ' + oCommandLineArguments.version)

        sUrl = extract_url(oCommandLineArguments)

        dHcmConfig = read_hcm_json_file(oCommandLineArguments.component)
        if not dHcmConfig:
            dHcmConfig = create_default_hcm_dictionary(oCommandLineArguments, sUrl)

        update_source_url(dHcmConfig)
        update_manifest(dHcmConfig)
        print dHcmConfig


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
