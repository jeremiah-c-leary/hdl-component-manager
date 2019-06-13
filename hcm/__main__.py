#!/usr/bin/env python

import argparse
import sys
import logging

from . import subcommand
from . import utils


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

    create_parser = subparsers.add_parser('create', help='Creates a component repo')
    install_parser = subparsers.add_parser('install', help='Adds a component from the component repo')
    list_parser = subparsers.add_parser('list', help='Lists components and their versions')
    publish_parser = subparsers.add_parser('publish', help='Adds components to the component repo')
    show_parser = subparsers.add_parser('show', help='Displays information about installed components')

    build_create_parser(create_parser)
    build_install_parser(install_parser)
    build_publish_parser(publish_parser)
    build_list_parser(list_parser)
    build_show_parser(show_parser)

    print_help_if_no_command_line_options_given(top_parser)

    oArgs = top_parser.parse_args()

    check_for_correctly_formed_version_argument(oArgs)

    return oArgs


def build_show_parser(oParser):
    oParser.add_argument('component', help='Component to display information')
    oParser.add_argument('--manifest', default=False, action='store_true', help='Displays manifest for all files in component')
    oParser.set_defaults(which='show')


def build_create_parser(oParser):
    oParser.add_argument('url', help='location to create the base component directory')
    oParser.set_defaults(which='create')


def build_install_parser(oParser):
    oParser.add_argument('component', help='Component name to install')
    oParser.add_argument('version', nargs='?', default=None, help='Major.Minor.Patch version of component to install.  Leave blank to install latest version.')
    oParser.add_argument('--url', help='location of component directory in repo')
    oParser.add_argument('--force', default=False, action='store_true', help='Install component ignoring any local changes')
    oParser.add_argument('--external', default=False, action='store_true', help='Install as an external')
    oParser.add_argument('--dependencies', default=False, action='store_true', help='Install dependencies')
    oParser.add_argument('--upgrade', default=False, action='store_true', help='Upgrade dependencies to latest version')
    oParser.set_defaults(which='install')


def build_list_parser(oParser):
    oParser.add_argument('--all', default=False, action='store_true', help='Includes directories that are not under HCM control')
    oParser.set_defaults(which='list')


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
    if oArgs.which == 'install':
        if oArgs.version is None:
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

    if commandLineArguments.which == 'create':
        subcommand.create(commandLineArguments.url)
    if commandLineArguments.which == 'publish':
        subcommand.publish(commandLineArguments)
    if commandLineArguments.which == 'install':
        subcommand.install(commandLineArguments)
    if commandLineArguments.which == 'list':
        subcommand.sub_list(commandLineArguments)
    if commandLineArguments.which == 'show':
        subcommand.show(commandLineArguments)

    sys.exit(0)


if __name__ == '__main__':
    main()
