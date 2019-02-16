#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import shutil
import stdlib
from core.log import wlog

_current_build = None


class Build():
    def __init__(self, manifest, version_data):
        self.manifest = manifest
        self.version_data = version_data
        self.semver = version_data['semver']
        self.major = version_data['semver'].split('.')[0]
        self.minor = version_data['semver'].split('.')[1]
        self.patch = version_data['semver'].split('.')[2]

        from core.cache import get_download_cache, get_build_cache, get_install_cache
        self.download_cache = get_download_cache(self)
        self.build_cache = get_build_cache(self)
        self.install_cache = get_install_cache(self)

        os.makedirs(self.download_cache, exist_ok=True)

        if os.path.exists(self.build_cache):
            shutil.rmtree(self.build_cache)
        os.makedirs(self.build_cache)

        if os.path.exists(self.install_cache):
            shutil.rmtree(self.install_cache)
        os.makedirs(self.install_cache)

    def __str__(self):
        return f'''{self.manifest.name} ({self.semver})'''

    def is_empty(self):
        for _, _, filenames in os.walk(self.install_cache):
            if len(filenames):
                return False
        return True

    def warn_leftovers(self):
        for root, _, filenames in os.walk(self.install_cache):
            for filename in filenames:
                abs_path = os.path.join(root, filename)
                rpath = os.path.relpath(abs_path, self.install_cache)
                wlog(rpath)


def current_build() -> Build:
    global _current_build
    return _current_build


def _set_current_build(build: Build):
    global _current_build
    _current_build = build
