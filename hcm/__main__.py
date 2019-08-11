#!/usr/bin/env python

import argparse
import sys
import logging

from . import subcommand
from . import utils
from . import version


def parse_command_line_arguments():
    '''
    Parses the command line arguments and returns them.
    '''

    top_parser = argparse.ArgumentParser(
      prog='hcm',
      description='''Provides configuration management for HDL components.
                   '''
    )

    subparsers = top_parser.add_subparsers()

    browse_parser = subparsers.add_parser('browse', help='List components available for installation.')
    create_parser = subparsers.add_parser('create', help='Creates a component repo')
    download_parser = subparsers.add_parser('download', help='Downloads components without installing them.')
    install_parser = subparsers.add_parser('install', help='Adds a component from the component repo')
    uninstall_parser = subparsers.add_parser('uninstall', help='Removes installed components')
    list_parser = subparsers.add_parser('list', help='Lists components and their versions')
    publish_parser = subparsers.add_parser('publish', help='Adds components to the component repo')
    show_parser = subparsers.add_parser('show', help='Displays information about installed components')
    validate_parser = subparsers.add_parser('validate', help='Verifies manifest of installed component')
    version_parser = subparsers.add_parser('version', help='Displays HCM version information')

    build_browse_parser(browse_parser)
    build_create_parser(create_parser)
    build_download_parser(download_parser)
    build_install_parser(install_parser)
    build_uninstall_parser(uninstall_parser)
    build_publish_parser(publish_parser)
    build_list_parser(list_parser)
    build_show_parser(show_parser)
    build_validate_parser(validate_parser)
    build_version_parser(version_parser)

    print_help_if_no_command_line_options_given(top_parser)

    oArgs = top_parser.parse_args()

    return oArgs


def build_version_parser(oParser):
    oParser.set_defaults(which='version')


def build_validate_parser(oParser):
    oParser.add_argument('component', help='Component to display information')
    oParser.add_argument('--report', default=False, action='store_true', help='Reports differences')
    oParser.set_defaults(which='validate')


def build_show_parser(oParser):
    oParser.add_argument('component', help='Component to display information')
    oParser.add_argument('--manifest', default=False, action='store_true', help='Displays manifest for all files in component')
    oParser.add_argument('--upgrades', default=False, action='store_true', help='Lists upgrade versions and their log entries')
    oParser.add_argument('--updates', default=False, action='store_true', help='Lists versions with newer publishes and their log entries')
    oParser.add_argument('--modifications', default=False, action='store_true', help='Lists committed modifications for component')
    oParser.set_defaults(which='show')


def build_create_parser(oParser):
    oParser.add_argument('url', help='location to create the base component directory')
    oParser.set_defaults(which='create')


def build_download_parser(oParser):
    oParser.add_argument('component', help='Component name to publish')
    oParser.add_argument('version', help='Major.Minor.Patch version to publish')
    oParser.set_defaults(which='download')


def build_install_parser(oParser):
    oParser.add_argument('component', help='Component name to install')
    oParser.add_argument('--version', default=None, help='Major.Minor.Patch version of component to install.')
    oParser.add_argument('--url', help='location of component directory in repo')
    oParser.add_argument('--force', default=False, action='store_true', help='Install component ignoring any local changes')
    oParser.add_argument('--external', default=False, action='store_true', help='Install as an external')
    oParser.add_argument('--dependencies', default=False, action='store_true', help='Install dependencies')
    oParser.add_argument('--upgrade', default=False, action='store_true', help='Upgrade dependencies to latest version')
    oParser.set_defaults(which='install')


def build_uninstall_parser(oParser):
    oParser.add_argument('component', help='Installed Component name to install')
    oParser.set_defaults(which='uninstall')


def build_list_parser(oParser):
    oParser.add_argument('--all', default=False, action='store_true', help='Includes directories that are not under HCM control')
    oParser.set_defaults(which='list')


def build_browse_parser(oParser):
    oParser.add_argument('component', default=None, nargs='?', help='Component to browse')
    oParser.set_defaults(which='browse')


def build_publish_parser(oParser):
    oParser.add_argument('component', help='Component name to publish')
    oParser.add_argument('version', help='Major.Minor.Patch version to publish')
    oGroup = oParser.add_mutually_exclusive_group(required=True)
    oGroup.add_argument('-m', help='Commit message')
    oGroup.add_argument('-f', help='File to use as commit message')
    oParser.add_argument('--url', help='Base URL of the component repository')
    oParser.set_defaults(which='publish')


def print_help_if_no_command_line_options_given(oParser):
    '''
    Will print the help output if no command line arguments were given.
    '''
    if len(sys.argv) == 1:
        oParser.print_help()
        sys.exit(1)


def check_for_correctly_formed_version_argument(oArgs):
    '''
    Will exit if a malformed version is given in the --URL argument.
    '''
    if oArgs.which == 'install' and oArgs.version is None:
        return

    try:
        if not utils.validate_version(oArgs.version):
            logging.error('Version ' + oArgs.version + ' does not match Major.Minor.Patch format.')
            sys.exit(1)
    except AttributeError:
        pass


def main():
    '''
    Main routine of the HDL Component Manager (HCM) application.
    '''

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    commandLineArguments = parse_command_line_arguments()

    check_for_correctly_formed_version_argument(commandLineArguments)

    if commandLineArguments.which == 'browse':
        subcommand.browse(commandLineArguments)
    elif commandLineArguments.which == 'create':
        subcommand.create(commandLineArguments.url)
    elif commandLineArguments.which == 'download':
        subcommand.download(commandLineArguments)
    elif commandLineArguments.which == 'publish':
        subcommand.publish(commandLineArguments)
    elif commandLineArguments.which == 'install':
        subcommand.install(commandLineArguments)
    elif commandLineArguments.which == 'uninstall':
        subcommand.uninstall(commandLineArguments)
    elif commandLineArguments.which == 'list':
        subcommand.sub_list(commandLineArguments)
    elif commandLineArguments.which == 'show':
        subcommand.show(commandLineArguments)
    elif commandLineArguments.which == 'validate':
        subcommand.validate(commandLineArguments.component, commandLineArguments.report)
    elif commandLineArguments.which == 'version':
        version.print_version()

    sys.exit(0)


if __name__ == '__main__':
    main()
