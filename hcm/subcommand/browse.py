import logging

from hcm import svn
from hcm import utils


def browse(oCommandLineArguments):

    lUrls = utils.get_url_from_environment_variable()
    if lUrls is None:
        logging.error('Unknown path to component repository.')
        logging.error('Please set the HCM_URL_PATHS environment variable.')
        exit(1)

    if oCommandLineArguments.component is None:
        lComponents = get_components()
        print_components(lComponents)
    else:
        print(oCommandLineArguments.component + ' versions available:')
        print('')
        lUrls = utils.get_url_from_environment_variable()
        for sUrl in lUrls:
            sComponentUrl = sUrl + '/' + oCommandLineArguments.component
            if svn.does_directory_exist(sComponentUrl):
                lVersions = svn.get_component_published_versions(sComponentUrl)
                lVersions.reverse()
                for sVersion in lVersions:
                    sVersionUrl = sComponentUrl + '/' + sVersion
                    print('Version: ' + sVersion)
                    lOutput = svn.issue_command(['svn', 'log', '-l 1', sVersionUrl]).split('\n')
                    for sLine in lOutput:
                        print(sLine)


def get_components():
    lUrls = utils.get_url_from_environment_variable()
    lReturn = []
    for sUrl in lUrls:
        lComponents = svn.get_components_from_url(sUrl)
        for sComponent in lComponents:
            lReturn.append([sComponent, sUrl])
    lReturn.sort()
    return lReturn


def get_maximum_component_length(lComponents):
    iReturn = len('Component')
    for lComp in lComponents:
        iReturn = max(iReturn, len(lComp[0]))
    return iReturn 


def get_maximum_url_length(lComponents):
    iReturn = 0
    for lComp in lComponents:
        iReturn = max(iReturn, len(lComp[1]))
    return iReturn


def print_components(lComponents):

    iComponentLength = get_maximum_component_length(lComponents)
    iUrlLength = get_maximum_url_length(lComponents)
    sRow = build_row(iComponentLength, len('00.00.00'), iUrlLength)

    print('')
    print(sRow.format('Component', 'Version', 'URL'))
    print(build_divider(sRow, iComponentLength, len('00.00.00'), iUrlLength))

    for lComp in lComponents:
        sVersion = utils.get_latest_version(lComp[1] + '/' + lComp[0])
        print(sRow.format(lComp[0], sVersion, lComp[1]))


def build_row(iComponentLength, iVersionLength, iUrlLength):
    sSpacer = '     '
    sComponentColumn = '{0:' + str(iComponentLength) + 's}'
    sVersionColumn = '{1:' + str(iVersionLength) + 's}'
    sUrlColumn = '{2:' + str(iUrlLength) + 's}'
    return sComponentColumn + sSpacer + sVersionColumn + sSpacer + sUrlColumn


def build_divider(sRow, iComponentLength, iVersionLength, iUrlLength):
    sComponent = '-' * iComponentLength
    sVersion = '-' * iVersionLength
    sUrl = '-' * iUrlLength
    return sRow.format(sComponent, sVersion, sUrl)
