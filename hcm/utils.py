
import os
import re
import yaml

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
