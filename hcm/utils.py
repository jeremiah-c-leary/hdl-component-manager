
import os
import re
import yaml
import logging
import subprocess
import json

from hcm import svn


def get_version_path(dHcmConfig):
    sUrl = get_component_path(dHcmConfig)
    sUrl += '/' + dHcmConfig['version']
    return sUrl


def get_component_name(dHcmConfig):
    return dHcmConfig['name']


def get_component_path(dHcmConfig):
    sUrl = get_url(dHcmConfig)
    sUrl += '/' + get_component_name(dHcmConfig)
    return sUrl


def get_url(dHcmConfig):
    return dHcmConfig['publish']['url']


def get_source_url(dHcmConfig):
    return dHcmConfig['source']['url']


def get_version(dHcmConfig):
    return dHcmConfig['version']


def get_manifest(dHcmConfig):
    return dHcmConfig['source']['manifest']


def get_hcm_config_path(dHcmConfig):
    return get_component_name(dHcmConfig) + '/hcm.json'


def get_url_from_environment_variable():
    try:
        return os.environ['HCM_URL_PATHS'].split(',')
    except KeyError:
        return None


def validate_version(sVersion):
    if re.match('^[0-9]+\.[0-9]+\.[0-9]+$', sVersion):
        return True
    return False


def get_latest_version(sUrl):
    try:
        lOutput = svn.issue_command(['svn', 'list', sUrl]).split('\n')[:-1]
        sUpgradeVersion = lOutput[-1][:-1]
        return sUpgradeVersion
    except IndexError:
        return 'None'


def read_dependencies(sDirectory):
    sFileName = sDirectory + '/dependencies.yaml'
    if not os.path.isfile(sFileName):
        return None
    try:
        with open(sFileName) as yaml_file:
            tempConfiguration = yaml.full_load(yaml_file)
        return tempConfiguration
    except yaml.parser.ParserError:
        logging.error('Error in dependency file: ' + sFileName)
        exit()


def calculate_md5sum(sFileName):
    lOutput = subprocess.check_output(['md5sum', sFileName], stderr=subprocess.STDOUT).decode('ascii').split('\n')
    return lOutput[0].split()[0]


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


def is_hcm_json_file_valid(dHcmJsonFile):
    fReturn = True
    fReturn = check_publish_dictionary(fReturn, dHcmJsonFile)
    fReturn = check_name(fReturn, dHcmJsonFile)
    fReturn = check_version(fReturn, dHcmJsonFile)
    fReturn = check_source_dictionary(fReturn, dHcmJsonFile)
    return fReturn


def check_publish_dictionary(fReturn, dHcmJsonFile):
    if 'publish' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'publish\' key')
        fReturn = False
    else:
        if 'url' not in dHcmJsonFile['publish']:
            logging.warning('hcm.json file is missing the \'publish url\' key')
            fReturn = False
    return fReturn


def check_name(fReturn, dHcmJsonFile):
    return check_hcm_key(fReturn, dHcmJsonFile, 'name')


def check_version(fReturn, dHcmJsonFile):
    return check_hcm_key(fReturn, dHcmJsonFile, 'version')


def check_source_dictionary(fReturn, dHcmJsonFile):
    if 'source' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'source\' key')
        fReturn = False
    else:
        fReturn = check_source_url(fReturn, dHcmJsonFile)
        fReturn = check_source_manifest(fReturn, dHcmJsonFile)
    return fReturn


def check_source_url(fReturn, dHcmJsonFile):
    return check_hcm_source_key(fReturn, dHcmJsonFile, 'url')


def check_source_manifest(fReturn, dHcmJsonFile):
    return check_hcm_source_key(fReturn, dHcmJsonFile, 'manifest')


def check_hcm_key(fReturn, dHcmJsonFile, sKey):
    if sKey not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'' + sKey + '\' key')
        fReturn = False
    return fReturn


def check_hcm_source_key(fReturn, dHcmJsonFile, sKey):
    if sKey not in dHcmJsonFile['source']:
        logging.warning('hcm.json file is missing the \'source ' + sKey + '\' key')
        fReturn = False
    return fReturn


def validate_urls(lUrl, sComponent, sVersion):
    fUrlPathFound = False
    fMultipleFound = False

    for sUrl in lUrl:
        sUrlPath = build_url_path(sUrl, sComponent, sVersion)
        if svn.does_directory_exist(sUrlPath):
            fMultipleFound = fUrlPathFound
            fUrlPathFound = True
            sFinalUrlPath = sUrlPath

    report_if_url_path_exists(fUrlPathFound, sComponent, lUrl)
    report_if_multiple_url_paths_exist(fMultipleFound, sComponent)

    return sFinalUrlPath


def report_if_url_path_exists(fUrlPathFound, sComponent, lUrl):
    if not fUrlPathFound:
        logging.error('Component ' + sComponent + ' could not be found in the following URLs:')
        for sUrl in lUrl:
            print(sUrl)
        exit()


def report_if_multiple_url_paths_exist(fMultipleFound, sComponent):
    if fMultipleFound:
        logging.warning('Component ' + sComponent + ' was found in multiple locations.')
        logging.info('Specify url using the --url command line argument.')
        exit()


def build_url_path(sUrl, sComponent, sVersion):
    sReturn = sUrl + '/' + sComponent + '/'
    if sVersion is None:
        try:
            return sReturn + get_latest_version(sUrl + '/' + sComponent)
        except:
            return None
    else:
        return sReturn + sVersion


def determine_url(sUrl=None):
    if sUrl:
        return [sUrl]

    lUrl = get_url_from_environment_variable()

    if lUrl is None:
        logging.error('URL path to components has not been specified.')
        logging.error('Use the --url option or set the HCM_URL_PATHS environment variable.')
        exit()

    return lUrl
