
import subprocess
import os


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

    dSvnRepos['http://svn/external_repo'] = []
    dSvnRepos['http://svn/external_repo'].append('comps/king')
    dSvnRepos['http://svn/external_repo'].append('comps/king/1.0.0')
    dSvnRepos['http://svn/external_repo'].append('comps/king/1.1.0')
    dSvnRepos['http://svn/external_repo'].append('comps/bishop')
    dSvnRepos['http://svn/external_repo'].append('comps/bishop/1.0.0')
    dSvnRepos['http://svn/external_repo'].append('comps/bishop/2.0.0')
    dSvnRepos['http://svn/external_repo'].append('comps/bishop/2.1.0')
    dSvnRepos['http://svn/external_repo'].append('comps/queen')
    dSvnRepos['http://svn/external_repo'].append('comps/queen/1.0.0')
    dSvnRepos['http://svn/external_repo'].append('comps/queen/2.0.0')
    dSvnRepos['http://svn/external_repo'].append('comps/queen/3.0.0')


    try:
        if lList[0] == 'mkdir':
            parse_svn_mkdir_command(lList[1:], dSvnRepos)
        if lList[0] == 'list':
            return parse_svn_list_command(lList[-1], dSvnRepos)
        if lList[0] == 'info':
            return parse_svn_info_command(lList[-1])
        if lList[0] == 'add':
            return parse_svn_add_command(lList[-1])
        if lList[0] == 'status':
            return parse_svn_status_command(lList[-1])
        if lList[0] == 'delete':
            return parse_svn_delete_command(lList[-1])
        if lList[0] == 'copy':
            return parse_svn_copy_command(lList[1:], dSvnRepos)
        if lList[0] == 'export':
            return parse_svn_copy_command(lList[1:], dSvnRepos)
        if lList[0] == 'propget' and lList[1] == 'svn:externals':
            return parse_svn_externals_command(lList[2])


    except subprocess.CalledProcessError as e:
        raise e


def parse_svn_externals_command(sDirectory):
    if sDirectory == '.':
        sReturn = 'http://svn/external_repo/blocks/castle/1.0.0 castle\n'
        sReturn += 'http://svn/external_repo/blocks/pawn/3.0.0 pawn\n'
        return sReturn
    else:
        return None


def parse_svn_copy_command(lArgs, dSvnRepos):
    if lArgs[0].startswith('http:'):
        sRepoUrl = lArgs[0]
        sLocalDir = lArgs[1]
    else:
        sRepoUrl = lArgs[1]
        sLocalDir = lArgs[0]

    fRepoUrlFound = False
    for sKey in dSvnRepos.keys():
        for sDir in dSvnRepos[sKey]:

            if sRepoUrl == sKey + '/' + sDir:
                fRepoUrlFound = True
                break

    if lArgs[0].startswith('http:'):
        if not fRepoUrlFound:
            raise subprocess.CalledProcessError(0, 'svn copy')
        os.mkdir(sLocalDir)
    else:
        if fRepoUrlFound:
            raise subprocess.CalledProcessError(0, 'svn copy')

    return True



def parse_svn_delete_command(sDirectory):
    if sDirectory == 'rook' or sDirectory == 'queen' or sDirectory == 'bishop':
        sReturn = 'D         ' + sDirectory + '\n'
        sReturn += 'D         ' + sDirectory + '/hcm.json\n'
        sReturn += 'D         ' + sDirectory + '/rtl\n'
        sReturn += 'D         ' + sDirectory + '/rtl/' + sDirectory + '.rtl\n'
        try:
            os.rmdir(sDirectory)
        except FileNotFoundError:
            pass
        return sReturn
    else:
        raise subprocess.CalledProcessError(0, 'svn delete')


def parse_svn_status_command(sDirectory):
    if sDirectory == 'rook' or sDirectory == 'queen' or sDirectory == 'bishop':
        return ''
    else:
        sReturn = '?   ' + sDirectory + '.vhd\n'
        sReturn += 'A   file.txt\n'
        sReturn += 'K   otherfile.xls\n'
        return sReturn


def parse_svn_add_command(sFileName):
    return True


def parse_svn_list_command(sUrl, dSvnRepos):
    fFoundUrl = False
    fFoundDirectory = False
    sOutput = ''
    for sKey in dSvnRepos.keys():
        if sUrl.startswith(sKey):
            fFoundUrl = True
            sDirectory = sUrl.replace(sKey + '/', '')
            if sDirectory in dSvnRepos[sKey]:
                fFoundDirectory = True
#                break
        for sUrlKey in dSvnRepos[sKey]:
            sUrlPath = sKey + '/' + sUrlKey
            if sUrlPath.startswith(sUrl + '/'):
                sOutput += sUrlPath.split('/')[-1] + '/\n'

    if not fFoundUrl:
        raise subprocess.CalledProcessError(0, 'svn list')

    if not fFoundDirectory:
        raise subprocess.CalledProcessError(0, 'svn list')
    return sOutput

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
    if sDirectory == 'rook':
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
    elif sDirectory == '.':
        sReturn = 'Path: .\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 7\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 7\n'
        sReturn += 'Last Changed Date: 2019-05-19 18:03:12 -0500 (Sun, 19 May 2019)\n'
        sReturn += '\n'

    return sReturn
