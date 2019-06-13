
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

    for sKey in dConfig['hcm']:
        iColumn1Max = max(iColumn1Max, len(sKey))
        iColumn2Max = max(iColumn2Max, len(dConfig['hcm'][sKey]))

    sRow = build_row(iColumn1Max, iColumn2Max) 

    print(build_divider(sRow, iColumn1Max, iColumn2Max))
    print(sRow.format('Component', dConfig['hcm']['name']))
    print(sRow.format('Version', dConfig['hcm']['version']))
    print(sRow.format('URL', dConfig['hcm']['url']))
    print(sRow.format('Source', dConfig['hcm']['source_url']))
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
    for sFileName in dConfig['hcm']['manifest']:
        iColumn1Max = max(iColumn1Max, len(dConfig['hcm']['manifest'][sFileName]))
        iColumn2Max = max(iColumn2Max, len(sFileName))

    print('\nManifest')
    print('-'*(iColumn1Max + len(sSpacer) + iColumn2Max))
    for sFileName in dConfig['hcm']['manifest']:
        print(dConfig['hcm']['manifest'][sFileName] + sSpacer + sFileName)


def get_dependencies(oCommandLineArguments):
    dDependencies = utils.read_dependencies(oCommandLineArguments.component)
    if dDependencies is None:
        return None
    return ', '.join(dDependencies['requires'].keys())
