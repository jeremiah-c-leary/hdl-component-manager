#!/usr/bin/env python

import argparse
import sys
import os
import shutil
import yaml


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
    update_parser = subparsers.add_parser('update', help='Updates a component to the requested version')

    create_parser.add_argument('url', help='location to create the base component repo')

    install_parser.add_argument('url', help='location of component in component repo')
    install_parser.add_argument('--version', help='Major.Minor.Patch version of component to update to')

    publish_parser.add_argument('component', help='Component name to publish')
    publish_parser.add_argument('version', help='Major.Minor.Patch version to publish')

    list_parser.add_argument('--upgrades', help='Lists upgrades for currently installed components')
    list_parser.add_argument('--available', help='Lists available components stored in repo')

    update_parser.add_argument('component', help='Component name to update')
    update_parser.add_argument('version', help='Major.Minor.Patch version of component to update to')

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

    sys.exit(0)


if __name__ == '__main__':
    main()
