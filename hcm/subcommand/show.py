
import json
import logging
import re

from hcm import utils
from hcm import svn


def show(oCommandLineArguments):

    sHcmJsonName = oCommandLineArguments.component + '/hcm.json'
    try:
        with open(sHcmJsonName) as json_file:
            dConfig = json.load(json_file)
    except IOError:
        logging.error('Component ' + oCommandLineArguments.component + ' is not under HCM control.')
        exit()

    sDependencies = get_dependencies(oCommandLineArguments)
    iColumn1Max = len('Dependencies')
    if sDependencies is None:
        sDependencies = 'No dependencies found'
    iColumn2Max = len(sDependencies)
    iColumn2Max = max(iColumn2Max, len(utils.get_component_name(dConfig)))
    iColumn2Max = max(iColumn2Max, len(utils.get_version(dConfig)))
    iColumn2Max = max(iColumn2Max, len(utils.get_url(dConfig)))
    iColumn2Max = max(iColumn2Max, len(utils.get_source_url(dConfig)))

    sRow = build_row(iColumn1Max, iColumn2Max)

    print(build_divider(sRow, iColumn1Max, iColumn2Max))
    print(sRow.format('Component', utils.get_component_name(dConfig)))
    print(sRow.format('Version', utils.get_version(dConfig)))
    print(sRow.format('URL', utils.get_url(dConfig)))
    print(sRow.format('Source', utils.get_source_url(dConfig)))
    print(sRow.format('Dependencies', sDependencies))
    print(build_divider(sRow, iColumn1Max, iColumn2Max))

    print_upgrades(oCommandLineArguments, dConfig)

    print_manifest(oCommandLineArguments, dConfig)

    print_uncommitted_modifications(oCommandLineArguments)
    print_committed_modifications(oCommandLineArguments)


def build_row(iColumn1Length, iColumn2Length):
    sSpacer = '     '
    sColumn1 = '{0:' + str(iColumn1Length) + 's}'
    sColumn2 = '{1:' + str(iColumn2Length) + 's}'
    return sColumn1 + sSpacer + sColumn2


def build_divider(sRow, iColumn1Length, iColumn2Length):
    sColumn1Divider = '-' * iColumn1Length
    sColumn2Divider = '-' * iColumn2Length
    return sRow.format(sColumn1Divider, sColumn2Divider)


def print_manifest(oCommandLineArguments, dConfig):
    if not oCommandLineArguments.manifest:
        return
    sSpacer = '    '
    iColumn1Max = 0
    iColumn2Max = 0
    dFiles = utils.get_manifest(dConfig)
    for sFileName in dFiles.keys():
        iColumn1Max = max(iColumn1Max, len(dFiles[sFileName]))
        iColumn2Max = max(iColumn2Max, len(sFileName))

    print('\nManifest')
    print('-'*(iColumn1Max + len(sSpacer) + iColumn2Max))
    for sFileName in dFiles.keys():
        print(dFiles[sFileName] + sSpacer + sFileName)


def get_dependencies(oCommandLineArguments):
    dDependencies = utils.read_dependencies(oCommandLineArguments.component)
    if dDependencies is None:
        return None
    return ', '.join(dDependencies['requires'].keys())


def print_upgrades(oCommandLineArguments, dConfig):
    if not oCommandLineArguments.upgrades:
        return

    print('')
    print('Available Upgrades')
    print('==================')
    lVersions = svn.get_component_published_versions(utils.get_component_path(dConfig))
    if utils.get_version(dConfig) == lVersions[-1]:
        print('No Upgrades')
        return

    lVersions.reverse()

    iIndex = lVersions.index(utils.get_version(dConfig))

    for sVersion in lVersions[:iIndex]:
        print('')
        print('Version: ' + sVersion)
        lOutput = svn.get_svn_log_stopped_on_copy(utils.get_component_path(dConfig) + '/' + sVersion)
        for sLine in lOutput:
            print(sLine)


def print_committed_modifications(oCommandLineArguments):
    if not oCommandLineArguments.modifications:
        return

    print('')
    print('Committed Modifications')
    print('=======================')

    lVersions = svn.get_svn_log_stopped_on_copy(oCommandLineArguments.component)
    iNumberRevisions = svn.number_of_revisions(lVersions)

    if iNumberRevisions == 1:
        print('No Committed Modifications')
        return

    iRevisions = 0
    for sVersion in lVersions:
        increment_revision(iRevisions, sVersion)
        if iRevisions == iNumberRevisions:
            break
        print(sVersion)


def increment_revision(iRevision, sVersion):
    if re.match('^r[0-9]+ ', sVersion):
        iRevision += 1


def print_uncommitted_modifications(oCommandLineArguments):
    if not oCommandLineArguments.modifications:
        return

    print('')
    print('Uncommitted Modifications')
    print('=========================')

    lStatus = svn.get_svn_status_of_directory(oCommandLineArguments.component)

    if lStatus == []:
        print('No Uncommitted Modifications')
        return

    for sStatus in lStatus:
        print(sStatus)
