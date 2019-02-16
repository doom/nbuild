#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import sys
import argparse

nbuild_args = None
nbuild_parser = None


def parse_args():
    global nbuild_parser
    global nbuild_args

    nbuild_parser = argparse.ArgumentParser(
        description='Compiles packages from a Build Manifest.'
    )
    nbuild_parser.add_argument(
        '-o',
        '--output-dir',
        default=os.path.join(
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'packages',
        ),
        help='Output directory for built packages. Default: packages/',
    )
    nbuild_parser.add_argument(
        '-c',
        '--cache-dir',
        default=os.path.join(
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'cache',
        ),
        help='Cache directory used when downloading and building packages. Default: cache/',
    )
    nbuild_parser.add_argument(
        '--purge',
        action='store_true',
        help='Remove all cached data.',
    )
    nbuild_parser.add_argument(
        '-r',
        '--repository',
        default='stable',
        metavar='REPOSITORY',
        help='Name of the repository built packages will be part of. Default: stable',
    )
    nbuild_parser.add_argument(
        '--name',
        metavar='BUILD_NAME',
        help='Name of the build to resume, start at a given checkpoint or stop at a given checkpoint',
    )
    nbuild_parser.add_argument(
        '--resume',
        help='Continue the build at the last reached checkpoint.',
    )
    nbuild_parser.add_argument(
        '--start-checkpoint',
        help='Start the build at the given checkpoint',
    )
    nbuild_parser.add_argument(
        '--stop-checkpoint',
        help='Stop the build at the given checkpoint',
    )
    nbuild_parser.add_argument(
        'manifest',
        metavar='MANIFEST_PATH',
        nargs='?',
    )
    nbuild_parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Make the operation more talkative. Append it multiple times to make it even more talkative.'
    )
    nbuild_args = nbuild_parser.parse_args()


def get_args():
    return nbuild_args


def get_parser():
    return nbuild_parser


def print_help():
    nbuild_parser.print_help()
