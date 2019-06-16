
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
    try:
        return dHcmConfig['publish']['url']
    except KeyError as e:
        raise e


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
    lOutput = svn.issue_command(['svn', 'list', sUrl]).split('\n')[:-1]
    sUpgradeVersion = lOutput[-1][:-1]
    return sUpgradeVersion


def read_dependencies(sDirectory):
    sFileName = sDirectory + '/dependencies.yaml'
    if not os.path.isfile(sFileName):
        return None
    try:
        with open(sFileName) as yaml_file:
            tempConfiguration = yaml.full_load(yaml_file)
        return tempConfiguration
    except:
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
    if 'publish' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'publish\' key')
        fReturn = False
    else:
        if 'url' not in dHcmJsonFile['publish']:
            logging.warning('hcm.json file is missing the \'publish url\' key')
            fReturn = False

    if 'name' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'name\' key')
        fReturn = False

    if 'version' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'version\' key')
        fReturn = False

    if 'source' not in dHcmJsonFile:
        logging.warning('hcm.json file is missing the \'source\' key')
        fReturn = False
    else:
        if 'url' not in dHcmJsonFile['source']:
            logging.warning('hcm.json file is missing the \'source url\' key')
            fReturn = False
        if 'manifest' not in dHcmJsonFile['source']:
            logging.warning('hcm.json file is missing the \'source manifest\' key')
            fReturn = False

    return fReturn
