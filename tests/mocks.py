
import subprocess


def mocked_subprocess_check_output(lList, stderr=None):
    try:
        if lList[0] == 'svn':
            parse_svn_command(lList[1:])
    except subprocess.CalledProcessError as e:
        raise e


def parse_svn_command(lList):
    dSvnRepos = {}
    dSvnRepos['http://svn/my_repo'] = []
    dSvnRepos['http://svn/my_repo'].append('components')
    dSvnRepos['http://svn/my_repo'].append('components/rook')
    dSvnRepos['http://svn/my_repo'].append('components/rook/1.0.0')
    dSvnRepos['http://svn/my_repo'].append('components/rook/1.1.0')
    dSvnRepos['http://svn/my_repo'].append('components/rook/2.0.0')
    dSvnRepos['http://svn/my_repo'].append('components/queen')
    dSvnRepos['http://svn/my_repo'].append('components/queen/1.0.0')
    dSvnRepos['http://svn/my_repo'].append('components/queen/2.0.0')
    dSvnRepos['http://svn/my_repo'].append('components/queen/3.0.0')

    try:
        if lList[0] == 'mkdir':
            parse_svn_mkdir_command(lList[1:], dSvnRepos)
        if lList[0] == 'list':
            parse_svn_list_command(lList[-1], dSvnRepos)
    except subprocess.CalledProcessError as e:
        raise e


def parse_svn_list_command(sUrl, dSvnRepos):
    fFoundUrl = False
    fFoundDirectory = False
    for sKey in dSvnRepos.keys():
        if sUrl.startswith(sKey):
            fFoundUrl = True
            sDirectory = sUrl.replace(sKey + '/', '')
            if sDirectory in dSvnRepos[sKey]:
                fFoundDirectory = True
                break

    if not fFoundUrl:
        raise subprocess.CalledProcessError(0, 'svn list')

    if not fFoundDirectory:
        raise subprocess.CalledProcessError(0, 'svn list')


def parse_svn_mkdir_command(lList, dSvnRepos):

    # Find URL string in command
    for sItem in lList:
        if sItem.startswith('-'):
            continue
        sUrl = sItem
    # check if url
    fFoundUrl = False
    fFoundDirectory = False
    for sKey in dSvnRepos.keys():
        if sUrl.startswith(sKey):
            fFoundUrl = True
            sPath = sUrl.replace(sKey + '/', '')
            if sPath in dSvnRepos[sKey]:
                fFoundDirectory = True
                break

    if not fFoundUrl:
        raise subprocess.CalledProcessError(0, 'svn mkdir')

    if fFoundDirectory:
        raise subprocess.CalledProcessError(0, 'svn mkdir')


