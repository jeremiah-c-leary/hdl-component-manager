
import logging
import os

from hcm import utils


def validate(sComponent):

        logging.info('Validating component ' + sComponent)

        dHcmJsonFile = utils.read_hcm_json_file(sComponent)

        dManifest = generate_manifest(sComponent)

        logging.info('Comparing manifest against installed component.')

        if dHcmJsonFile['source']['manifest'] != dManifest:
            logging.error('Installed component does not match manifest.')
            exit(1)
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
