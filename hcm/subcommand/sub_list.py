
import os
import json
import logging

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

    lExternals = parse_externals_into_components()

    for sDirectory in lDirectories:

        if not svn.is_directory_under_svn_control(sDirectory):
            add_non_svn_controlled_directory(dVersions, sDirectory, lExternals, oCommandLineArguments)
            continue

        update_column_width(dVersions, 'max_comp_len', len(sDirectory))

        add_hcm_controlled_component(dVersions, sDirectory, lExternals)
        add_non_hcm_controlled_component(dVersions, sDirectory, lExternals, oCommandLineArguments)

    print_versions(dVersions)


def add_hcm_controlled_component(dVersions, sDirectory, lExternals):
    sHcmName = sDirectory + '/hcm.json'
    if os.path.isfile(sHcmName):
        dConfig = read_hcm_json_file(sHcmName)
        if svn.does_directory_exist(utils.get_component_path(dConfig)):
            dVersions['components'][sDirectory] = {}
            copy_url(dVersions, dConfig, sDirectory)
            copy_version(dVersions, dConfig, sDirectory)
            update_column_width(dVersions, 'max_ver_len', len(utils.get_version(dConfig)))
            update_column_width(dVersions, 'max_url_len', len(utils.get_url(dConfig)))
            sUpgrade = str(get_upgrade(utils.get_component_path(dConfig), utils.get_version(dConfig)))
            dVersions['components'][sDirectory]['upgrade'] = sUpgrade
            update_column_width(dVersions, 'max_upgrade_len', len(sUpgrade))

            update_external(dVersions, sDirectory, lExternals)
        else:
            dVersions['components'][sDirectory] = {}
            dVersions['components'][sDirectory]['url'] = 'Invalid'
            dVersions['components'][sDirectory]['version'] = 'None'
            dVersions['components'][sDirectory]['upgrade'] = 'None'

            update_external(dVersions, sDirectory, lExternals)


def add_non_hcm_controlled_component(dVersions, sDirectory, lExternals, oCommandLineArguments):
    sHcmName = sDirectory + '/hcm.json'
    if oCommandLineArguments.all and not os.path.isfile(sHcmName):
        add_blank_entry(dVersions, sDirectory)
        update_external(dVersions, sDirectory, lExternals)


def add_non_svn_controlled_directory(dVersions, sDirectory, lExternals, oCommandLineArguments):
    if oCommandLineArguments.all:
        add_blank_entry(dVersions, sDirectory)
        update_external(dVersions, sDirectory, lExternals)


def add_blank_entry(dVersions, sDirectory):
    dVersions['components'][sDirectory] = {}
    dVersions['components'][sDirectory]['url'] = '-----'
    dVersions['components'][sDirectory]['version'] = '-----'
    dVersions['components'][sDirectory]['upgrade'] = '-----'


def read_hcm_json_file(sHcmName):
    try:
        with open(sHcmName) as json_file:
            dConfig = json.load(json_file)
    except ValueError:
        logging.error('Invalid JSON formatted file: ' + sHcmName)
        exit(1)
    if not utils.is_hcm_json_file_valid(dConfig):
        logging.error(sHcmName + ' is missing information')
        exit(1)
    return dConfig


def parse_externals_into_components():
    lExternals = []
    try:
        for sLine in svn.get_externals('.').split('\n')[:-1]:
            lLine = sLine.split()
            lExternals.append(lLine[-1])
    except AttributeError:
        pass
    except IndexError:
        pass

    return lExternals


def update_external(dVersions, sComponent, lExternals):
    if sComponent in lExternals:
        dVersions['components'][sComponent]['External'] = True
    else:
        dVersions['components'][sComponent]['External'] = False


def copy_version(dVersions, dConfig, sDirectory):
    dVersions['components'][sDirectory]['version'] = utils.get_version(dConfig)


def copy_url(dVersions, dConfig, sDirectory):
    dVersions['components'][sDirectory]['url'] = utils.get_url(dConfig)


def update_column_width(dVersions, sKey, iValue):
    dVersions['config'][sKey] = max(dVersions['config'][sKey], iValue)


def get_directories():
    lDirectories = os.listdir('.')
    lDirectories.sort()
    lReturn = []
    for sDirectory in lDirectories:
        if os.path.isdir(sDirectory):
            lReturn.append(sDirectory)
    return lReturn


def print_versions(dVersions):
    lKeys = list(dVersions['components'].keys())
    lKeys.sort()

    dConfig = dVersions['config']

    sRow = build_row(dConfig['max_comp_len'], dConfig['max_ver_len'], dConfig['max_upgrade_len'], dConfig['max_url_len'])

    print('')
    print(sRow.format('Component', 'Version', 'Upgrade', 'Status', 'URL'))
    print(build_divider(sRow, dVersions))

    for sKey in lKeys:
        sVersion = dVersions['components'][sKey]['version']
        sUrl = dVersions['components'][sKey]['url']
        sStatus = update_status_field(dVersions, sKey)
        sUpgrade = str(dVersions['components'][sKey]['upgrade'])
        print(sRow.format(sKey, sVersion, sUpgrade, sStatus, sUrl))


def update_status_field(dVersions, sComponent):

        sStatus = update_external_status_flag(dVersions, sComponent)
        sStatus += update_committed_modifications_status_flag(dVersions, sComponent)
        sStatus += update_uncommitted_modifications_status_flag(sComponent)
        sStatus += update_svn_control_status_flag(dVersions, sComponent)
        return sStatus


def update_external_status_flag(dVersions, sComponent):
    if dVersions['components'][sComponent]['External']:
        return 'E'
    else:
        return ' '


def update_committed_modifications_status_flag(dVersions, sComponent):
    if dVersions['components'][sComponent]['url'] == '-----':
        return ' '

    if svn.directory_has_committed_modifications(sComponent):
        return 'M'
    else:
        return ' '


def update_uncommitted_modifications_status_flag(sComponent):
    if not svn.is_directory_under_svn_control(sComponent):
        return ' '

    if svn.does_directory_have_uncommitted_files(sComponent):
        return 'U'
    else:
        return ' '


def update_svn_control_status_flag(dVersions, sComponent):
    if not svn.is_directory_under_svn_control(sComponent):
        return 'N'
    else:
        return ' '


def build_row(iComponentLength, iVersionLength, iUpgradeLength, iUrlLength):
    sSpacer = '     '
    sComponentColumn = '{0:' + str(iComponentLength) + 's}'
    sVersionColumn = '{1:' + str(iVersionLength) + 's}'
    sUpgradeColumn = '{2:' + str(iUpgradeLength) + 's}'
    sStatusColumn = '{3:' + str(len('Status')) + 's}'
    sUrlColumn = '{4:' + str(iUrlLength) + 's}'
    return sComponentColumn + sSpacer + sVersionColumn + sSpacer + sUpgradeColumn + sSpacer + sStatusColumn + sSpacer + sUrlColumn


def build_divider(sRow, dVersions):
    sComponent = '-' * dVersions['config']['max_comp_len']
    sVersion = '-' * dVersions['config']['max_ver_len']
    sUpgrade = '-' * dVersions['config']['max_upgrade_len']
    sStatus = '-' * len('Status')
    sUrl = '-' * dVersions['config']['max_url_len']
    return sRow.format(sComponent, sVersion, sUpgrade, sStatus, sUrl)


def get_upgrade(sUrl, sVersion):
    sUpgradeVersion = utils.get_latest_version(sUrl)
    if sVersion == sUpgradeVersion:
        return None
    else:
        return sUpgradeVersion
