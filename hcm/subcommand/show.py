
import json
import logging

from hcm import utils


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

    print_manifest(oCommandLineArguments, dConfig)


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
