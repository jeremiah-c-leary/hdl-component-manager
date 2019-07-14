
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
    dSvnRepos['http://svn/my_repo'].append('components/pawwn')

    dSvnRepos['http://svn/external_repo'] = []
    dSvnRepos['http://svn/external_repo'].append('comps')
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
            return parse_svn_delete_command(lList[1:])
        if lList[0] == 'copy':
            return parse_svn_copy_command(lList[1:], dSvnRepos)
        if lList[0] == 'export':
            return parse_svn_copy_command(lList[1:], dSvnRepos)
        if lList[0] == 'propget' and lList[1] == 'svn:externals':
            return parse_svn_externals_command(lList[2])
        if lList[0] == 'log':
            return parse_svn_log_command(lList[1:])


    except subprocess.CalledProcessError as e:
        raise e


def parse_svn_log_command(lArgs):
    if 'http://svn/my_repo/comps/rook' in lArgs or \
       'http://svn/my_repo/components/rook/2.0.0' in lArgs or \
       'http://svn/my_repo/components/rook/1.1.0' in lArgs or \
       'http://svn/my_repo/components/rook/1.0.0' in lArgs:
        sOutput = '------------------------------------------------------------------------\n'
        sOutput += 'r10 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line\n'
        sOutput += '\n'
        sOutput += 'initial release\n'
        sOutput += '------------------------------------------------------------------------\n'
        if lArgs[0] == '--stop-on-copy' or lArgs[0] == '-l 1':
            return sOutput
        sOutput += 'r8 | jeremiah | 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019) | 2 lines\n'
        sOutput += '\n'
        sOutput += 'Adding rook.\n'
        sOutput += '\n'
        sOutput += '------------------------------------------------------------------------\n'

        return sOutput
    elif 'rook' in lArgs:
        sOutput = '------------------------------------------------------------------------\n'
        sOutput += 'r11 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line\n'
        sOutput += '\n'
        sOutput += 'initial release\n'
        sOutput += '------------------------------------------------------------------------\n'
        sOutput += 'r8  | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line\n'
        sOutput += '\n'
        sOutput += 'initial release\n'
        sOutput += '------------------------------------------------------------------------\n'
        if lArgs[0] == '--stop-on-copy':
            return sOutput
        sOutput += 'r8 | jeremiah | 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019) | 2 lines\n'
        sOutput += '\n'
        sOutput += 'Adding rook.\n'
        sOutput += '\n'
        sOutput += '------------------------------------------------------------------------\n'

        return sOutput
    elif 'queen' in lArgs:
        sOutput = '------------------------------------------------------------------------\n'
        sOutput += 'r11 | jeremiah | 2019-05-20 21:39:51 -0500 (Mon, 20 May 2019) | 1 line\n'
        sOutput += '\n'
        sOutput += 'initial release\n'
        sOutput += '------------------------------------------------------------------------\n'
        if lArgs[0] == '--stop-on-copy':
            return sOutput
        sOutput += 'r8 | jeremiah | 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019) | 2 lines\n'
        sOutput += '\n'
        sOutput += 'Adding rook.\n'
        sOutput += '\n'
        sOutput += '------------------------------------------------------------------------\n'

        return sOutput



def parse_svn_externals_command(sDirectory):
    if sDirectory == '.':
        sReturn = 'http://svn/external_repo/blocks/castle/1.0.0 castle\n'
        sReturn += 'http://svn/external_repo/blocks/pawn/3.0.0 pawn\n'
        return sReturn
    else:
        raise subprocess.CalledProcessError(0, 'svn propget')


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



def parse_svn_delete_command(lArgs):
    sDirectory = lArgs[0]
    fForce = False
    if len(lArgs) > 1:
        fForce = lArgs[1]

    if sDirectory == 'rook' or sDirectory == 'queen' or sDirectory == 'bishop' or fForce:
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
        sReturn = ''
    elif sDirectory == 'castle':
        sReturn = 'A  +    castle\n'
        sReturn += '?       castle/rtl/movement.vhd\n'
        sReturn += 'M  +    castle/rtl/castle-rtl.vhd\n'
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
    iNumberOfLevels = sUrl.count('/') + 1
    for sKey in dSvnRepos.keys():
        if sUrl.startswith(sKey):
            fFoundUrl = True
            sDirectory = sUrl.replace(sKey + '/', '')
            if sDirectory in dSvnRepos[sKey]:
                fFoundDirectory = True
#                break
        for sUrlKey in dSvnRepos[sKey]:
            sUrlPath = sKey + '/' + sUrlKey
#            print(str(iNumberOfLevels) + ' | ' + str(sUrlPath.count('/')) + ' | ' + sUrlPath)
            if sUrlPath.startswith(sUrl + '/') and iNumberOfLevels == sUrlPath.count('/'):
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
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 39\n'
        sReturn += 'Last Changed Date: 2019-06-02 11:08:07 -0500 (Sun, 02 Jun 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: rook/hcm.json\n'
        sReturn += 'Name: hcm.json\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/hcm.json\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/hcm.json\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 30\n'
        sReturn += 'Last Changed Date: 2019-05-28 18:46:35 -0500 (Tue, 28 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-01 19:46:44 -0500 (Sat, 01 Jun 2019)\n'
        sReturn += 'Checksum: 1cdb07bdade9b553afbba6002358a632bb3abd88\n'
        sReturn += '\n'
        sReturn += 'Path: rook/lay\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/lay\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/lay\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 8\n'
        sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: rook/lay/filelist.tcl\n'
        sReturn += 'Name: filelist.tcl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/lay/filelist.tcl\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/lay/filelist.tcl\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 8\n'
        sReturn += 'Last Changed Date: 2019-05-19 18:42:49 -0500 (Sun, 19 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-01 19:46:44 -0500 (Sat, 01 Jun 2019)\n'
        sReturn += 'Checksum: 8ab4b37511ade8aa5f322015ba1881baa715842a\n'
        sReturn += '\n'
        sReturn += 'Path: rook/rtl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/rtl\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/rtl\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 30\n'
        sReturn += 'Last Changed Date: 2019-05-28 18:46:35 -0500 (Tue, 28 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: rook/rtl/rook.vhd\n'
        sReturn += 'Name: rook.vhd\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/rook/rtl/rook.vhd\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/rook/rtl/rook.vhd\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 39\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 40\n'
        sReturn += 'Last Changed Date: 2019-06-02 11:12:32 -0500 (Sun, 02 Jun 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-02 11:10:40 -0500 (Sun, 02 Jun 2019)\n'
        sReturn += 'Checksum: a81c71c718ad4c19516aa5f3fdae93f143ada337\n'
        sReturn += '\n'
    elif sDirectory == 'queen':
        sReturn = 'Path: queen\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/queen\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/queen\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 38\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 18\n'
        sReturn += 'Last Changed Date: 2019-05-21 21:01:22 -0500 (Tue, 21 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: queen/lay\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/queen/lay\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/queen/lay\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 38\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 18\n'
        sReturn += 'Last Changed Date: 2019-05-21 21:01:22 -0500 (Tue, 21 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: queen/lay/filelist.tcl\n'
        sReturn += 'Name: filelist.tcl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/queen/lay/filelist.tcl\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/queen/lay/filelist.tcl\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 38\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 18\n'
        sReturn += 'Last Changed Date: 2019-05-21 21:01:22 -0500 (Tue, 21 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-01 06:28:35 -0500 (Sat, 01 Jun 2019)\n'
        sReturn += 'Checksum: ca901804d426b01466072e99191f85d32648f3f2\n'
        sReturn += '\n'
        sReturn += 'Path: queen/rtl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/queen/rtl\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/queen/rtl\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 38\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 18\n'
        sReturn += 'Last Changed Date: 2019-05-21 21:01:22 -0500 (Tue, 21 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: queen/rtl/queen.rtl\n'
        sReturn += 'Name: queen.rtl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess\n'
        sReturn += 'URL: http://svn/my_repo/trunk/project_chess/components/queen/rtl/queen.rtl\n'
        sReturn += 'Relative URL: ^/trunk/project_chess/components/queen/rtl/queen.rtl\n'
        sReturn += 'Repository Root: http://svn/my_repo\n'
        sReturn += 'Repository UUID: 321bcf6c-b4d1-4a84-b4b7-55c366bdaac7\n'
        sReturn += 'Revision: 38\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 18\n'
        sReturn += 'Last Changed Date: 2019-05-21 21:01:22 -0500 (Tue, 21 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-01 06:28:35 -0500 (Sat, 01 Jun 2019)\n'
        sReturn += 'Checksum: 728a202fce6192598616453b79425c4c97737eb7\n'
        sReturn += '\n'
    elif sDirectory == 'pawn':
        sReturn = 'Path: pawn\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess/components/pawn\n'
        sReturn += 'URL: http://svn/external_repo/blocks/pawn/1.0.0\n'
        sReturn += 'Relative URL: ^/blocks/pawn/1.0.0\n'
        sReturn += 'Repository Root: http://svn/external_repo\n'
        sReturn += 'Repository UUID: 5f2de28d-62b4-4c7b-be41-96622ff69593\n'
        sReturn += 'Revision: 10\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 6\n'
        sReturn += 'Last Changed Date: 2019-05-29 21:45:44 -0500 (Wed, 29 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: pawn/hcm.json\n'
        sReturn += 'Name: hcm.json\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess/components/pawn\n'
        sReturn += 'URL: http://svn/external_repo/blocks/pawn/1.0.0/hcm.json\n'
        sReturn += 'Relative URL: ^/blocks/pawn/1.0.0/hcm.json\n'
        sReturn += 'Repository Root: http://svn/external_repo\n'
        sReturn += 'Repository UUID: 5f2de28d-62b4-4c7b-be41-96622ff69593\n'
        sReturn += 'Revision: 10\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 5\n'
        sReturn += 'Last Changed Date: 2019-05-29 21:45:44 -0500 (Wed, 29 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-02 11:02:00 -0500 (Sun, 02 Jun 2019)\n'
        sReturn += 'Checksum: bd2b33b61df24415c678f26bc3d1e978dc3fdc4c\n'
        sReturn += '\n'
        sReturn += 'Path: pawn/rtl\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess/components/pawn\n'
        sReturn += 'URL: http://svn/external_repo/blocks/pawn/1.0.0/rtl\n'
        sReturn += 'Relative URL: ^/blocks/pawn/1.0.0/rtl\n'
        sReturn += 'Repository Root: http://svn/external_repo\n'
        sReturn += 'Repository UUID: 5f2de28d-62b4-4c7b-be41-96622ff69593\n'
        sReturn += 'Revision: 10\n'
        sReturn += 'Node Kind: directory\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 3\n'
        sReturn += 'Last Changed Date: 2019-05-29 21:42:53 -0500 (Wed, 29 May 2019)\n'
        sReturn += '\n'
        sReturn += 'Path: pawn/rtl/pawn.vhd\n'
        sReturn += 'Name: pawn.vhd\n'
        sReturn += 'Working Copy Root Path: /home/jeremiah/projects/hdl-component-manager/project_chess/components/pawn\n'
        sReturn += 'URL: http://svn/external_repo/blocks/pawn/1.0.0/rtl/pawn.vhd\n'
        sReturn += 'Relative URL: ^/blocks/pawn/1.0.0/rtl/pawn.vhd\n'
        sReturn += 'Repository Root: http://svn/external_repo\n'
        sReturn += 'Repository UUID: 5f2de28d-62b4-4c7b-be41-96622ff69593\n'
        sReturn += 'Revision: 10\n'
        sReturn += 'Node Kind: file\n'
        sReturn += 'Schedule: normal\n'
        sReturn += 'Last Changed Author: jeremiah\n'
        sReturn += 'Last Changed Rev: 3\n'
        sReturn += 'Last Changed Date: 2019-05-29 21:42:53 -0500 (Wed, 29 May 2019)\n'
        sReturn += 'Text Last Updated: 2019-06-02 11:02:00 -0500 (Sun, 02 Jun 2019)\n'
        sReturn += 'Checksum: 0500570aedd1bf70b0b43f4d66bddacbeb47920e\n'
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
    elif sDirectory == 'unknown':
        sReturn = 'This is just for testing the list subcommand with the --all option.\n'
    else:
        raise subprocess.CalledProcessError(0, 'svn info')

    return sReturn
