#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import random
from core.args import get_args
from stdlib.build import Build
from stdlib.package import Package


def get_install_cache(build: Build):
    return os.path.join(
        get_args().cache_dir,
        'install',
        build.manifest.name,
        build.semver,
    )


def get_download_cache(build: Build):
    return os.path.join(
        get_args().cache_dir,
        'download',
        build.manifest.name,
        build.semver,
    )


def get_build_cache(build: Build):
    return os.path.join(
        get_args().cache_dir,
        'build',
        build.manifest.name,
        build.semver,
    )


def get_wrap_cache(package: Package):
    return os.path.join(
        get_args().cache_dir,
        'wrap',
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def get_package_cache(package: Package):
    return os.path.join(
        get_args().output_dir,
        package.id.repository,
        package.id.category,
        package.id.name,
        package.id.version,
    )


def purge_cache():
    folder = get_args().cache_dir

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
        except Exception:
            pass
