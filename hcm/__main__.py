#!/usr/bin/env python

import argparse
import sys
import logging

import subcommand


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

    create_parser = subparsers.add_parser('create', help='creates a component repo')
    install_parser = subparsers.add_parser('install', help='adds a component from the component repo')
    list_parser = subparsers.add_parser('list', help='lists components and their versions')
    publish_parser = subparsers.add_parser('publish', help='Adds components to the component repo')

    create_parser.add_argument('url', help='location to create the base component directory')
    create_parser.set_defaults(which='create')

    install_parser.add_argument('component', help='Component name to install')
    install_parser.add_argument('version', help='Major.Minor.Patch version of component to install, or latest to grab the latest version.')
    install_parser.add_argument('--url', help='location of component directory in repo')
    install_parser.set_defaults(which='install')

    publish_parser.add_argument('component', help='Component name to publish')
    publish_parser.add_argument('version', help='Major.Minor.Patch version to publish')
    publish_parser.add_argument('-m', required=True, help='Commit message')
    publish_parser.add_argument('--url', help='Base URL of the component repository')
    publish_parser.set_defaults(which='publish')

    list_parser.add_argument('--upgrades', default=False, action='store_true', help='Lists upgrades for currently installed components')
    list_parser.set_defaults(which='list')

    if len(sys.argv) == 1:
        top_parser.print_help()
        sys.exit(1)
    else:
        return top_parser.parse_args()


def main():
    '''
    Main routine of the HDL Component Manager (HCM) application.
    '''

    commandLineArguments = parse_command_line_arguments()

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    if commandLineArguments.which == 'create':
        subcommand.create(commandLineArguments.url)
    if commandLineArguments.which == 'publish':
        subcommand.publish(commandLineArguments)
    if commandLineArguments.which == 'install':
        subcommand.install(commandLineArguments.url, commandLineArguments.component, commandLineArguments.version)
    if commandLineArguments.which == 'list':
        subcommand.sub_list()

    sys.exit(0)


if __name__ == '__main__':
    main()
