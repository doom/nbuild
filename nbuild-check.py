#!/usr/bin/env python3

import argparse
import importlib.util
import nbuild.checks.base as base
from nbuild.checks import check_package
from nbuild.manifest import load_manifest
from nbuild.stdenv.build import Build, current_build, set_current_build
from nbuild.args import set_args


def parse_args():
    parser = argparse.ArgumentParser(
        description="Checks package compiled with nbuild",
    )
    parser.add_argument(
        'manifests',
        nargs='*',
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
            '--fix',
            action='store_true',
            help="Set the action to FIX (default)",
    )
    group.add_argument(
            '--edit',
            action='store_true',
            help="Set the action to EDIT",
    )
    group.add_argument(
            '--diff',
            action='store_true',
            help="Set the action to DIFF",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    set_args(args)

    if args.diff:
        base.Check.global_state = base.Type.DIFF
    elif args.edit:
        base.Check.global_state = base.Type.EDIT
    else:
        base.Check.global_state = base.Type.FIX

    print(base.Check.global_state)

    for manifest_path in args.manifests:
        spec = load_manifest(manifest_path)
        set_current_build(Build())
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for pkg in current_build().packages:
            check_package(pkg)


if __name__ == '__main__':
    main()
