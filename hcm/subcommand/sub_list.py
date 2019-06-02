
import os
import json

from hcm import svn
from hcm import utils


def sub_list(oCommandLineArguments):

    lDirectories = get_directories()

    dVersions = {}
    dVersions['components'] = {}
    dVersions['config'] = {}
    dVersions['config']['max_comp_len'] = len('Component')
    dVersions['config']['max_ver_len'] = len('99.99.99')
    dVersions['config']['max_url_len'] = len('-----')
    dVersions['config']['max_upgrade_len'] = len('99.99.99')

    lExternals = []
    for sLine in svn.get_externals('.').split('\n')[:-1]:
        if sLine is not '':
            lLine = sLine.split()
            lExternals.append(lLine[-1])

    print(lExternals)

    for sDirectory in lDirectories:
        update_column_width(dVersions, 'max_comp_len', len(sDirectory))
        sHcmName = sDirectory + '/hcm.json'
        
        if os.path.isfile(sHcmName):
            with open(sHcmName) as json_file:
                dConfig = json.load(json_file)
            dVersions['components'][sDirectory] = {}
            copy_key(dVersions, dConfig, sDirectory, 'url')
            copy_key(dVersions, dConfig, sDirectory, 'version')
            update_column_width(dVersions, 'max_ver_len', len(dConfig['hcm']['version']))
            update_column_width(dVersions, 'max_url_len', len(dConfig['hcm']['url']))
            sUpgrade = str(get_upgrade(utils.get_component_path(dConfig), dConfig['hcm']['version']))
            dVersions['components'][sDirectory]['upgrade'] = sUpgrade
            update_column_width(dVersions, 'max_upgrade_len', len(sUpgrade))

            if sDirectory in lExternals:
                dVersions['components'][sDirectory]['External'] = True
            else:
                dVersions['components'][sDirectory]['External'] = False

        elif oCommandLineArguments.all:
            dVersions['components'][sDirectory] = {}
            dVersions['components'][sDirectory]['url'] = '-----'
            dVersions['components'][sDirectory]['version'] = '-----'
            dVersions['components'][sDirectory]['upgrade'] = '-----'


    print_versions(dVersions)


def copy_key(dVersions, dConfig, sDirectory, sKey):
    dVersions['components'][sDirectory][sKey] = dConfig['hcm'][sKey]


def update_column_width(dVersions, sKey, iValue):
    dVersions['config'][sKey] = max(dVersions['config'][sKey], iValue)


def get_directories():
    lDirectories = os.listdir('.')
    lDirectories.sort()
    return lDirectories


def print_versions(dVersions):
    lKeys = dVersions['components'].keys()
    lKeys.sort()

    sRow = build_row(dVersions['config']['max_comp_len'], dVersions['config']['max_ver_len'], dVersions['config']['max_upgrade_len'], dVersions['config']['max_url_len'])

    print('')
    print(sRow.format('Component', 'Version', 'Upgrade', 'Status', 'URL'))
    print(build_divider(sRow, dVersions))

    for sKey in lKeys:
        sVersion = dVersions['components'][sKey]['version']
        sUrl = dVersions['components'][sKey]['url']
        if dVersions['components'][sKey]['External']:
            sStatus = 'E'
        else:
            sStatus = ' '
        sUpgrade = str(dVersions['components'][sKey]['upgrade'])
        print(sRow.format(sKey, sVersion, sUpgrade, sStatus, sUrl))


def build_row(iComponentLength, iVersionLength, iUpgradeLength, iUrlLength):
    sSpacer = '     '
    sComponentColumn = '{0:' + str(iComponentLength) + 's}'
    sVersionColumn = '{1:' + str(iVersionLength) + 's}'
    sUpgradeColumn = '{2:' + str(iUpgradeLength) + 's}'
    sStatusColumn = '{3:' + str(len('Status')) + 's}'
    sUrlColumn = '{4:' + str(iUrlLength) + 's}'
    return sComponentColumn + sSpacer + sVersionColumn + sSpacer + sUpgradeColumn + sSpacer + sStatusColumn + sSpacer + sUrlColumn


def build_divider(sRow, dVersions):
    return sRow.format('-' * dVersions['config']['max_comp_len'], '-' * dVersions['config']['max_ver_len'], '-' * dVersions['config']['max_upgrade_len'], '-' * len('Status'), '-' * dVersions['config']['max_url_len'])


def get_upgrade(sUrl, sVersion):
    lOutput = svn.issue_command(['svn', 'list', sUrl]).split('\n')[:-1]
    sUpgradeVersion = lOutput[-1][:-1]
    if sVersion == sUpgradeVersion:
        return None
    else:
        return lOutput[-1][:-1]
