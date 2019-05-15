#!/usr/bin/env python3

import argparse
import importlib.util
import stdlib.checks.base as base
from stdlib.checks.check import set_check
from stdlib.checks import check_package
from stdlib.build import Build, current_build, _set_current_build
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
        '-o',
        '--output-dir',
        default='packages/',
        help="Output directory for built packages",
    )
    parser.add_argument(
        '-c',
        '--cache-dir',
        default='cache/',
        help="Cache directory used when downloading and building packages",
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help="Make the operation more talkative",
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
    core.args._set_args(args)
    set_check()

    if args.diff:
        base.Check.global_state = base.Type.DIFF
    elif args.edit:
        base.Check.global_state = base.Type.EDIT
    elif args.fix:
        base.Check.global_state = base.Type.FIX

    manifest_path = args.manifest
    spec = importlib.util.spec_from_file_location('build_manifest', manifest_path)
    if not spec:
        stdlib.log.flog(f"Failed to load Build Manifest located at path \"{manifest_path}\"")
        exit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # for manifest_path in args.manifests:
    #     spec = load_manifest(manifest_path)
    #     # _set_current_build(Build(), )
    #     module = importlib.util.module_from_spec(spec)
    #     spec.loader.exec_module(module)

    #     for pkg in current_build().packages:
    #         check_package(pkg)


if __name__ == '__main__':
    main()
