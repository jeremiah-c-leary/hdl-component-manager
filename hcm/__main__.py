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

    build_browse_parser(subparsers)
    build_create_parser(subparsers)
    build_download_parser(subparsers)
    build_install_parser(subparsers)
    build_uninstall_parser(subparsers)
    build_publish_parser(subparsers)
    build_list_parser(subparsers)
    build_show_parser(subparsers)
    build_validate_parser(subparsers)
    build_version_parser(subparsers)

    print_help_if_no_command_line_options_given(top_parser)

    oArgs = top_parser.parse_args()

    return oArgs


def build_version_parser(oSubparser):
    version_parser = oSubparser.add_parser('version', help='Displays HCM version information')

    version_parser.set_defaults(which='version')


def build_validate_parser(oSubparser):
    validate_parser = oSubparser.add_parser('validate', help='Verifies manifest of installed component')

    validate_parser.add_argument('component', help='Component to display information')
    validate_parser.add_argument('--report', default=False, action='store_true', help='Reports differences')
    validate_parser.set_defaults(which='validate')


def build_show_parser(oSubparser):
    show_parser = oSubparser.add_parser('show', help='Displays information about installed components')

    show_parser.add_argument('component', help='Component to display information')
    show_parser.add_argument('--manifest', default=False, action='store_true', help='Displays manifest for all files in component')
    show_parser.add_argument('--upgrades', default=False, action='store_true', help='Lists upgrade versions and their log entries')
    show_parser.add_argument('--updates', default=False, action='store_true', help='Lists versions with newer publishes and their log entries')
    show_parser.add_argument('--modifications', default=False, action='store_true', help='Lists committed modifications for component')
    show_parser.set_defaults(which='show')


def build_create_parser(oSubparser):
    create_parser = oSubparser.add_parser('create', help='Creates a component repo')

    create_parser.add_argument('url', help='location to create the base component directory')
    create_parser.set_defaults(which='create')


def build_download_parser(oSubparser):
    download_parser = oSubparser.add_parser('download', help='Downloads components without installing them.')

    download_parser.add_argument('component', help='Component name to publish')
    download_parser.add_argument('version', help='Major.Minor.Patch version to publish')
    download_parser.set_defaults(which='download')


def build_install_parser(oSubparser):
    install_parser = oSubparser.add_parser('install', help='Adds a component from the component repo')

    install_parser.add_argument('component', help='Component name to install')
    install_parser.add_argument('--version', default=None, help='Major.Minor.Patch version of component to install.')
    install_parser.add_argument('--url', help='location of component directory in repo')
    install_parser.add_argument('--force', default=False, action='store_true', help='Install component ignoring any local changes')
    install_parser.add_argument('--external', default=False, action='store_true', help='Install as an external')
    install_parser.add_argument('--dependencies', default=False, action='store_true', help='Install dependencies')
    install_parser.add_argument('--upgrade', default=False, action='store_true', help='Upgrade dependencies to latest version')
    install_parser.set_defaults(which='install')


def build_uninstall_parser(oSubparser):
    uninstall_parser = oSubparser.add_parser('uninstall', help='Removes installed components')

    uninstall_parser.add_argument('component', help='Installed Component name to install')
    uninstall_parser.set_defaults(which='uninstall')


def build_list_parser(oSubparser):
    list_parser = oSubparser.add_parser('list', help='Lists components and their versions')

    list_parser.add_argument('--all', default=False, action='store_true', help='Includes directories that are not under HCM control')
    list_parser.set_defaults(which='list')


def build_browse_parser(oSubparser):
    browse_parser = oSubparser.add_parser('browse', help='List components available for installation.')

    browse_parser.add_argument('component', default=None, nargs='?', help='Component to browse')
    browse_parser.set_defaults(which='browse')


def build_publish_parser(oSubparser):
    publish_parser = oSubparser.add_parser('publish', help='Adds components to the component repo')

    publish_parser.add_argument('component', help='Component name to publish')
    publish_parser.add_argument('version', help='Major.Minor.Patch version to publish')
    oGroup = publish_parser.add_mutually_exclusive_group(required=True)
    oGroup.add_argument('-m', help='Commit message')
    oGroup.add_argument('-f', help='File to use as commit message')
    publish_parser.add_argument('--url', help='Base URL of the component repository')
    publish_parser.set_defaults(which='publish')


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
