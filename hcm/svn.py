
import subprocess


def issue_command(lCommand):
    try:
        return subprocess.check_output(lCommand, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise e


def does_directory_exist(sUrl):
    try:
        issue_command(['svn', 'list', sUrl])
        return True
    except subprocess.CalledProcessError:
        return False


def mkdir(sUrl):
    try:
        issue_command(['svn', 'mkdir', '--parents', sUrl, '-m HCM: Creating componet directory.'])
        return True
    except subprocess.CalledProcessError as e:
        raise e
