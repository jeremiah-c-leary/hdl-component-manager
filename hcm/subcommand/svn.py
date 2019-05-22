
import subprocess


def does_directory_exist(sUrl):
    try:
        subprocess.check_output(['svn', 'list', sUrl], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False


def mkdir(sUrl):
    try:
        subprocess.check_output(['svn', 'mkdir', '--parents', sUrl, '-m HCM: Creating componet directory.'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise e
