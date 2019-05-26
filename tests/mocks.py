
import subprocess


def mocked_subprocess_check_output(lList, stderr=None):
    try:
        if lList[0] == 'svn':
            return parse_svn_command(lList[1:])
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
        if lList[0] == 'info':
            return parse_svn_info_command(lList[-1])
        if lList[0] == 'add':
            return parse_svn_add_command(lList[-1])
    except subprocess.CalledProcessError as e:
        raise e


def parse_svn_add_command(sFileName):
    return True
    

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

def parse_svn_info_command(sDirectory):
    sReturn = 'Path: rook\n'
    sReturn += 'Working Copy Root Path: /project_chess\n'
    sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook\n'
    sReturn += 'Relative URL: ^/trunk/project_chess/components/rook\n'
    sReturn += 'Repository Root: http://svn/my_repo\n'
    sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
    sReturn += 'Revision: 8\n'
    sReturn += 'Node Kind: directory\n'
    sReturn += 'Schedule: normal\n'
    sReturn += 'Last Changed Author: jeremiah\n'
    sReturn += 'Last Changed Rev: 8\n'
    sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
    sReturn += '\n'
    sReturn += 'Path: rook/lay\n'
    sReturn += 'Working Copy Root Path: /project_chess\n'
    sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/lay\n'
    sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/lay\n'
    sReturn += 'Repository Root: http://svn/my_repo\n'
    sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
    sReturn += 'Revision: 8\n'
    sReturn += 'Node Kind: directory\n'
    sReturn += 'Schedule: normal\n'
    sReturn += 'Last Changed Author: jeremiah\n'
    sReturn += 'Last Changed Rev: 8\n'
    sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
    sReturn += '\n'
    sReturn += 'Path: rook/lay/filelist.tcl\n'
    sReturn += 'Name: filelist.tcl\n'
    sReturn += 'Working Copy Root Path: /project_chess\n'
    sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/lay/filelist.tcl\n'
    sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/lay/filelist.tcl\n'
    sReturn += 'Repository Root: http://svn/my_repo\n'
    sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
    sReturn += 'Revision: 8\n'
    sReturn += 'Node Kind: file\n'
    sReturn += 'Schedule: normal\n'
    sReturn += 'Last Changed Author: jeremiah\n'
    sReturn += 'Last Changed Rev: 8\n'
    sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
    sReturn += 'Text Last Updated: 2019-05-19 18:04:46 -0500 (Sun, 19 May 2019)\n'
    sReturn += 'Checksum: 8ab4b37511ade8aa5f322015ba1881baa715842a\n'
    sReturn += '\n'
    sReturn += 'Path: rook/rtl\n'
    sReturn += 'Working Copy Root Path: /project_chess\n'
    sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/rtl\n'
    sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/rtl\n'
    sReturn += 'Repository Root: http://svn/my_repo\n'
    sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
    sReturn += 'Revision: 8\n'
    sReturn += 'Node Kind: directory\n'
    sReturn += 'Schedule: normal\n'
    sReturn += 'Last Changed Author: jeremiah\n'
    sReturn += 'Last Changed Rev: 8\n'
    sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
    sReturn += '\n'
    sReturn += 'Path: rook/rtl/rook.vhd\n'
    sReturn += 'Name: rook.vhd\n'
    sReturn += 'Working Copy Root Path: /project_chess\n'
    sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/rtl/rook.vhd\n'
    sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/rtl/rook.vhd\n'
    sReturn += 'Repository Root: http://svn/my_repo\n'
    sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
    sReturn += 'Revision: 21\n'
    sReturn += 'Node Kind: file\n'
    sReturn += 'Schedule: normal\n'
    sReturn += 'Last Changed Author: jeremiah\n'
    sReturn += 'Last Changed Rev: 21\n'
    sReturn += 'Last Changed Date: 2019-05-20 21:54:20 -0500 (Mon, 20 May 2019)\n'
    sReturn += 'Text Last Updated: 2019-05-20 21:54:06 -0500 (Mon, 20 May 2019)\n'
    sReturn += 'Checksum: c2aeb8841cf4a7178d311e6cff353a31b00af89a\n'
    sReturn += '\n'

    return sReturn
