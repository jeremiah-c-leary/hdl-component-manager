
import logging
import os
import json


def sub_list(oCommandLineArguments):

    lDirectories = get_directories()

    dVersions = {}
    dVersions['components'] = {}
    dVersions['config'] = {}
    dVersions['config']['max_comp_len'] = len('Component')
    dVersions['config']['max_ver_len'] = len('99.99.99')
    dVersions['config']['max_url_len'] = len('-----')

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
            dVersions['config']['max_url_len'] = max(dVersions['config']['max_url_len'], len(dConfig['hcm']['url']))
        elif oCommandLineArguments.all:
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

    sRow = build_row(dVersions['config']['max_comp_len'], dVersions['config']['max_ver_len'], dVersions['config']['max_url_len'])

    print('')
    print(sRow.format('Component', 'Version', 'URL'))
    print(build_divider(sRow, dVersions))

    for sKey in lKeys:
        sVersion = dVersions['components'][sKey]['version']
        sUrl = dVersions['components'][sKey]['url']
        print(sRow.format(sKey, sVersion, sUrl))


def build_row(iComponentLength, iVersionLength, iUrlLength):
    sSpacer = '     '
    sComponentColumn = '{0:' + str(iComponentLength) + 's}'
    sVersionColumn = '{1:' + str(iVersionLength) + 's}'
    sUrlColumn = '{2:' + str(iUrlLength) + 's}'
    return sComponentColumn + sSpacer + sVersionColumn + sSpacer + sUrlColumn


def build_divider(sRow, dVersions):
    return sRow.format('-' * dVersions['config']['max_comp_len'], '-' * dVersions['config']['max_ver_len'], '-' * dVersions['config']['max_url_len'])
