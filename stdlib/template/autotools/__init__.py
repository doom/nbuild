#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import nbuild
import stdlib
import stdlib.fetch
import stdlib.extract
import stdlib.patch
import stdlib.split
from core.log import ilog

from stdlib.template.autotools.configure import configure
from stdlib.template.autotools.make import make


def build_library(
    build_folder='build',
    fetch=stdlib.fetch.fetch_data,
    extract=stdlib.extract.extract_tarballs,
    patch=stdlib.patch.apply_patches,
    configure=configure,
    compile=make,
    check=lambda: make(target='check', fail_ok = True),
    install=lambda: make(f'DESTDIR={stdlib.current_build().install_cache}', target='install'),
    split=lambda: stdlib.split.all_in_one_library(),
) -> stdlib.Aggregate:
    build = stdlib.current_build()
    pkgs = []

    ilog("Step 1/8: Fetch", indent=False)
    if fetch is not None:
        fetch()

    ilog("Step 2/8: Extract", indent=False)
    if extract is not None:
        extract()

    ilog("Step 3/8: Patch", indent=False)
    if patch is not None:
        patch()

    os.makedirs(build_folder, exist_ok=True)
    with stdlib.pushd(build_folder):
        os.environ['DESTDIR'] = build.install_cache

        ilog("Step 4/8: Configure", indent=False)
        if configure is not None:
            configure()

        ilog("Step 5/8: Compile", indent=False)
        if compile is not None:
            compile()

        ilog("Step 6/8: Check", indent=False)
        if check is not None:
            check()

        ilog("Step 7/8: Install", indent=False)
        if install is not None:
            install()

        ilog("Step 8/8: Split", indent=False)
        if split is not None:
            pkgs = split()

    return pkgs


def build_binary(
    build_folder='build',
    fetch=None,
    extract=stdlib.extract.extract_tarballs,
    patch=stdlib.patch.apply_patches,
    configure=configure,
    compile=make,
    check=lambda: make(target='check', fail_ok = True),
    install=lambda: make(f'DESTDIR={stdlib.current_build().install_cache}', target='install'),
    split=lambda: stdlib.split.all_in_one_binary(),
):
    build = stdlib.current_build()
    pkgs = []

    ilog("Step 1/8: Fetch", indent=False)
    if fetch is not None:
        fetch()

    ilog("Step 2/8: Extract", indent=False)
    if extract is not None:
        extract()

    ilog("Step 3/8: Patch", indent=False)
    if patch is not None:
        patch()

    os.makedirs(build_folder, exist_ok=True)
    with stdlib.pushd(build_folder):
        os.environ['DESTDIR'] = build.install_cache

        ilog("Step 4/8: Configure", indent=False)
        if configure is not None:
            configure()

        ilog("Step 5/8: Compile", indent=False)
        if compile is not None:
            compile()

        ilog("Step 6/8: Check", indent=False)
        if check is not None:
            check()

        ilog("Step 7/8: Install", indent=False)
        if install is not None:
            install()

        ilog("Step 8/8: Split", indent=False)
        if split is not None:
            pkgs = split()

    return pkgs
