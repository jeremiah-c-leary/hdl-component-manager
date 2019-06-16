
import logging
import os

import hcm.svn as svn


def uninstall(oCommandLineArguments):

    sComponent = oCommandLineArguments.component

    if svn.is_component_externalled(sComponent):
        svn.remove_external(sComponent)
        svn.update_current_directory()
        logging.info('Uninstalled component ' + sComponent)
    elif not os.path.isdir(sComponent):
        logging.warning('Component ' + sComponent + ' does not exist')
    elif svn.is_directory_under_svn_control(sComponent):
        svn.delete(sComponent, True)
        logging.info('Uninstalled component ' + sComponent)
    else:
        logging.warning('Component ' + sComponent + ' is not under SVN control')
