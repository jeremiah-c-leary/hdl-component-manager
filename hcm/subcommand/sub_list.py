
import logging
import os
import json

import hcm.svn as svn
import hcm.utils as utils


def sub_list():

    logging.info('Listing components')

    lDirectories = get_directories()

    iMaxComponentNameLength = 0

    dVersions = {}
    dVersions['components'] = {}
    dVersions['config'] = {}
    dVersions['config']['max_comp_len'] = len('Component')
    dVersions['config']['max_ver_len'] = len('99.99.99')

    for sDirectory in lDirectories:
        dVersions['config']['max_comp_len'] = max(dVersions['config']['max_comp_len'], len(sDirectory))
        sHcmName = sDirectory + '/hcm.json'
        if os.path.isfile(sHcmName):
            with open(sHcmName) as json_file:
                dConfig = json.load(json_file)
            dVersions['components'][sDirectory] = {}
            dVersions['components'][sDirectory]['url'] = dConfig['hcm']['url']
            dVersions['components'][sDirectory]['version'] = dConfig['hcm']['version']
            dVersions['config']['max_ver_len'] = max(dVersions['config']['max_ver_len'], len(dConfig['hcm']['version']))
        else:
            dVersions['components'][sDirectory] = {}
            dVersions['components'][sDirectory]['url'] = '-----'
            dVersions['components'][sDirectory]['version'] = '-----'

    print_versions(dVersions)


def get_directories():
    lDirectories = os.listdir('.')
    lDirectories.sort()
    return lDirectories


def print_versions(dVersions):
    lKeys = dVersions['components'].keys()
    lKeys.sort()

    sSpacer = '     ' 
    sComponentColumn = '{0:' + str(dVersions['config']['max_comp_len']) + 's}'
    sVersionColumn = '{0:' + str(dVersions['config']['max_ver_len']) + 's}'

    sComponentHeader = sComponentColumn.format('Component')
    sVersionHeader = sVersionColumn.format('Version')

    print('')
    print(sComponentHeader + sSpacer + sVersionHeader)
    print('-' * dVersions['config']['max_comp_len'] + sSpacer + '-' * dVersions['config']['max_ver_len'])

    for sKey in lKeys:
        sComponentName = sComponentColumn.format(sKey)
        sVersion = sVersionColumn.format(dVersions['components'][sKey]['version'])
        print(sComponentName + sSpacer + sVersion)

