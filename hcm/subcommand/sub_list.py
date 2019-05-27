
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

    for sDirectory in lDirectories:
        iMaxComponentNameLength = max(iMaxComponentNameLength, len(sDirectory))
        sHcmName = sDirectory + '/hcm.json'
        if os.path.isfile(sHcmName):
            with open(sHcmName) as json_file:
                dConfig = json.load(json_file)
            dVersions[sDirectory] = dConfig['hcm']['version']
        else:
            dVersions[sDirectory] = '-----'

    print_versions(dVersions)


def get_directories():
    lDirectories = os.listdir('.')
    lDirectories.sort()
    return lDirectories


def print_versions(dVersions):
    lKeys = dVersions.keys()
    lKeys.sort()

    for sKey in lKeys:
        print("{0:10s} : {1:10s}".format(sKey, dVersions[sKey]))

