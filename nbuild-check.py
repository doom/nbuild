#!/usr/bin/env python3

import os
import sys
import argparse
import importlib.util
import stdlib.checks.base as base
from stdlib.checks.check import set_check
import core.args
import stdlib.log


_is_check = False


def is_check():
    global is_check
    return is_check


def parse_args():
    parser = argparse.ArgumentParser(
        description="Checks package compiled with nbuild",
    )
    parser.add_argument(
        'manifest',
        nargs='?',
    )
    parser.add_argument(
        '--config',
        default=os.path.join(  # Default path is script_dir/config.toml
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'config.toml',
        ),
        help="Static configuration for Nest Build. Default: config.toml",
    )
    parser.add_argument(
        '-o',
        '--output-dir',
        default=os.path.join(  # Default path is script_dir/packages
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'packages',
        ),
        help="Output directory for built packages. Default: packages/",
    )
    parser.add_argument(
        '-c',
        '--cache-dir',
        default=os.path.join(  # Default path is script_dir/cache
            os.getcwd(),
            os.path.dirname(sys.argv[0]),
            'cache',
        ),
        help="Cache directory used when downloading and building packages. Default: cache/",
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help="Make the operation more talkative. Append it multiple times to make it even more talkative."
    )
    parser.add_argument(
        '--visual',
        action='store_true',
        help="Try to use more visual tools (only makes sense with --edit, which is by default)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            '--fix',
            action='store_true',
            help="Set the action to FIX",
    )
    group.add_argument(
            '--edit',
            action='store_true',
            help="Set the action to EDIT (default)",
    )
    group.add_argument(
            '--diff',
            action='store_true',
            help="Set the action to DIFF",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.manifest is None:
        stdlib.log.flog("No path to a build manifest given.")
        exit(1)
    core.args._set_args(args)
    set_check()

    if args.diff:
        base.Check.global_state = base.Type.DIFF
    elif args.edit:
        base.Check.global_state = base.Type.EDIT
    elif args.fix:
        base.Check.global_state = base.Type.FIX

    manifest_path = args.manifest

    try:
        core.config.load_config()
    except Exception as e:
        print('bonjour')
        stdlib.log.flog(str(e))
        exit(1)

    try:
        _ = core.config.get_config()['global']['target']
    except:
        stdlib.log.flog("The configuration file doesn't indicate the target repository.")
        exit(1)

    spec = importlib.util.spec_from_file_location('build_manifest', manifest_path)
    if not spec:
        stdlib.log.flog(f"Failed to load Build Manifest located at path \"{manifest_path}\"")
        exit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


if __name__ == '__main__':
    main()
