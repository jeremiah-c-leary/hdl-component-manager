
import logging
import os

from hcm import utils


def validate(sComponent, fReport):

    logging.info('Validating component ' + sComponent)

    dHcmJsonFile = utils.read_hcm_json_file(sComponent)

    dManifest = generate_manifest(sComponent)

    logging.info('Comparing manifest against installed component.')

    if utils.get_manifest(dHcmJsonFile) != dManifest:
        logging.error('Installed component does not match manifest.')
        if not fReport:
            exit(1)
        else:
            report_differences(dHcmJsonFile, dManifest)
    else:
        logging.info('Installed component matches manifest.')


def generate_manifest(sDirectory):

    dManifest = {}
    for root, dirs, files in os.walk(sDirectory, topdown=True):
        for name in files:
            sFileName = os.path.join(root, name)
            add_file_to_manifest(dManifest, sFileName)
    return dManifest


def add_file_to_manifest(dManifest, sFileName):
    if 'hcm.json' in sFileName:
        return False
    if '.svn' in sFileName:
        return False
    dManifest[sFileName] = utils.calculate_md5sum(sFileName)
    return True


def report_differences(dHcmJsonFile, dManifest):
    print('')
    print('Missing Files')
    for sFile in check_for_missing_files(dHcmJsonFile, dManifest):
        print('  ' + sFile)
    print('')

    print('Extra Files')
    for sFile in check_for_extra_files(dHcmJsonFile, dManifest):
        print('  ' + sFile)
    print('')

    print('Changed Files')
    for sFile in check_for_changed_files(dHcmJsonFile, dManifest):
        print('  ' + sFile)


def check_for_missing_files(dHcmJsonFile, dManifest):
    lReturn = []
    lKeys = dManifest.keys()
    for sKey in utils.get_manifest(dHcmJsonFile).keys():
        if sKey not in lKeys:
            lReturn.append(sKey)
    return lReturn


def check_for_extra_files(dHcmJsonFile, dManifest):
    lReturn = []
    lKeys = utils.get_manifest(dHcmJsonFile).keys()
    for sKey in dManifest.keys():
        if sKey not in lKeys:
            lReturn.append(sKey)
    return lReturn


def check_for_changed_files(dHcmJsonFile, dManifest):
    lReturn = []
    lKeys = dManifest.keys()
    dHcmJsonFileManifest = utils.get_manifest(dHcmJsonFile)
    for sKey in dHcmJsonFileManifest.keys():
        if is_file_missing(sKey, lKeys, dHcmJsonFileManifest, dManifest):
            lReturn.append(sKey)
    return lReturn


def is_file_missing(sFileName, lKeys, dHcmJsonFileManifest, dManifest):
    if sFileName in lKeys and dHcmJsonFileManifest[sFileName] != dManifest[sFileName]:
        return True
    return False
