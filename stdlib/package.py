#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import toml
import shutil
import os
import stdlib
import tarfile
import glob
import copy
from termcolor import colored
from braceexpand import braceexpand
from datetime import datetime
from core.args import get_args
from core.log import ilog, clog, dlog


class PackageId():
    def __init__(self, name, repository=None, category=None, version=None):
        build = stdlib.current_build()

        self.repository = repository if repository is not None else get_args().repository
        self.category = category if category is not None else build.manifest.category
        self.version = version if version is not None else build.semver
        self.name = name

    def full_name(self):
        return f'{self.repository}::{self.category}/{self.name}'

    def __str__(self):
        return f'{self.full_name()}#{self.version}'


class Package():
    def __init__(
        self,
        id: PackageId,
        description: str,
        maintainer: str = None,
        licenses: [stdlib.License] = None,
        upstream_url: str = None,
        run_dependencies: {} = dict(),
    ):
        from core.cache import get_wrap_cache, get_package_cache

        build = stdlib.current_build()

        self.id = id
        self.description = description.replace('\n', ' ').strip()
        self.maintainer = maintainer if maintainer is not None else build.manifest.maintainer
        self.licenses = licenses if licenses is not None else build.manifest.licenses
        self.upstream_url = upstream_url if upstream_url is not None else build.manifest.upstream_url
        self.run_dependencies = copy.deepcopy(run_dependencies)

        self.wrap_cache = get_wrap_cache(self)
        self.package_cache = get_package_cache(self)

        if os.path.exists(self.wrap_cache):
            shutil.rmtree(self.wrap_cache)
        os.makedirs(self.wrap_cache)

        if os.path.exists(self.package_cache):
            shutil.rmtree(self.package_cache)
        os.makedirs(self.package_cache)

    def rename(self, new_id: PackageId):
        from core.cache import get_wrap_cache, get_package_cache

        old_wrap_cache = self.wrap_cache
        old_package_cache = self.package_cache

        self.id = new_id
        self.wrap_cache = get_wrap_cache(self)
        self.package_cache = get_package_cache(self)

        # In addition to internalling renaming the package, we need to move the caches
        # to a location that matches its new name.

        if os.path.exists(self.wrap_cache):  # Erase any existing cache first
            shutil.rmtree(self.wrap_cache)
        os.makedirs(os.path.dirname(self.wrap_cache), exist_ok=True)  # Then create parent directories
        shutil.move(old_wrap_cache, self.wrap_cache)  # Finally, move the cache from its old to its new location

        if os.path.exists(self.package_cache):  # Same here
            shutil.rmtree(self.package_cache)
        os.makedirs(os.path.dirname(self.package_cache), exist_ok=True)
        shutil.move(old_package_cache, self.package_cache)

    def is_empty(self):
        for _, _, filenames in os.walk(self.wrap_cache):
            if len(filenames):
                return False
        return True

    def drain(self, *rglobs):
        build = stdlib.current_build()

        # Move to source directory
        with stdlib.pushd(build.install_cache):
            for rglob in rglobs:
                for rglob in braceexpand(rglob):  # Expand braces

                    if os.path.isabs(rglob):
                        raise RuntimeError("Package.drain() received an absolute path as parameter, but it expects a relative one")

                    for rpath in glob.glob(rglob):  # Expand globbing
                        dstpath = os.path.join(
                            self.wrap_cache,
                            os.path.relpath(
                                rpath,
                                build.install_cache
                            ),
                        )

                        os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                        shutil.move(rpath, dstpath)

    def drain_package(self, source: 'stdlib.Package', *rglobs):
        with stdlib.pushd(source.wrap_cache):
            for rglob in rglobs:
                for rglob in braceexpand(rglob):  # Expand braces

                    if os.path.isabs(rglob):
                        raise RuntimeError("Package.drain_package() received an absolute path as parameter, but it expects a relative one")

                    for rpath in glob.glob(rglob):  # Expand globbing
                        dstpath = os.path.join(
                            self.wrap_cache,
                            os.path.relpath(
                                rpath,
                                source.wrap_cache,
                            ),
                        )

                        os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                        shutil.move(rpath, dstpath)

    def drain_build_cache(self, *pairs):
        build = stdlib.current_build()

        # Move to source directory
        with stdlib.pushd(build.build_cache):
            for pair in pairs:

                if os.path.isabs(pair[1]):
                    raise RuntimeError("Package.drain_build_cache() received an absolute path as parameter, but it expects a relative one")

                for rglob in braceexpand(pair[0]):  # Expand braces

                    if os.path.isabs(rglob):
                        raise RuntimeError("Package.drain_build_cache() received an absolute path as parameter, but it expects a relative one")

                    for rpath in glob.glob(rglob):  # Expand globbing
                        dstpath = os.path.join(
                            self.wrap_cache,
                            pair[1],
                        )

                        os.makedirs(os.path.dirname(dstpath), exist_ok=True)  # Create parent directories (if any)
                        shutil.move(rpath, dstpath)

    def move(self, srcs: str, dst: str):
        if os.path.isabs(srcs):
            raise RuntimeError("Package.move() received an absolute path as parameter, but it expects a relative one")

        if os.path.isabs(dst):
            raise RuntimeError("Package.move() received an absolute path as parameter, but it expects a relative one")

        with stdlib.pushd(self.wrap_cache):
            for srcs in braceexpand(srcs):  # Expand braces
                for src in glob.glob(srcs):  # Expand globbing
                    os.makedirs(os.path.dirname(dst), exist_ok=True)  # Create parent directories (if any)
                    shutil.move(src, dst)

    def remove(self, srcs: str):
        if os.path.isabs(srcs):
            raise RuntimeError("Package.move() received an absolute path as parameter, but it expects a relative one")

        with stdlib.pushd(self.wrap_cache):
            for srcs in braceexpand(srcs):  # Expand braces
                for src in glob.glob(srcs):  # Expand globbing
                    if os.path.isdir(src):
                        shutil.rmtree(src)
                    else:
                        os.remove(src)

    def make_keepers(self, *keepers: str):
        for keeper in keepers:
            if os.path.isabs(keeper):
                raise RuntimeError("Package.make_keeper() received an absolute path as parameter, but it expects a relative one")

            path = os.path.join(
                self.wrap_cache,
                keeper,
                '.nestkeep',
            )
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w+')

    def make_symlinks(self, *links: (str, str)):
        for link in links:
            if os.path.isabs(link[1]):
                raise RuntimeError("Package.make_keeper() received an absolute path as parameter, but it expects a relative one")

            dst = os.path.join(
                self.wrap_cache,
                link[1],
            )

            os.symlink(link[0], dst)

    def depends_on(self, package: 'Package', version_req=None):
        if version_req is None:
            version_req = f'={package.id.version}'
        self.run_dependencies[package.id.full_name()] = version_req

    def __get_colored_path(self, path, pretty_path=None):
        if pretty_path is None:
            pretty_path = path

        if os.path.islink(path):
            target_path = os.path.join(
                os.path.dirname(path),
                os.readlink(path),
            )
            if os.path.exists(target_path):
                return f"{colored(path, 'cyan', attrs=['bold'])} -> {self.__get_colored_path(target_path, os.readlink(path))}"
            else:
                return f"{colored(path, on_color='on_red', attrs=['bold'])} -> {colored(os.readlink(path), on_color='on_red', attrs=['bold'])}"
        elif os.path.isdir(path):
            return colored(pretty_path, 'blue', attrs=['bold'])
        elif os.access(path, os.X_OK):
            return colored(pretty_path, 'green', attrs=['bold'])
        else:
            return pretty_path

    def wrap(self):
        clog(f"Wrapping {self.id} ({self.wrap_cache})", indent=False)

        with stdlib.pushd(self.wrap_cache):
            files_count = 0
            clog("Files added:", indent=False)
            for root, _, filenames in os.walk('.'):
                for filename in filenames:
                    clog(self.__get_colored_path(os.path.join(root, filename)))
                    files_count += 1
            clog(f"(That's {files_count} files.)", indent=False)

            ilog("Creating data.tar.gz", indent=False)
            tarball_path = os.path.join(self.package_cache, 'data.tar.gz')
            with tarfile.open(tarball_path, mode='w:gz') as archive:
                archive.add('./')

        ilog("Creating manifest.toml", indent=False)
        toml_path = os.path.join(self.package_cache, 'manifest.toml')
        with open(toml_path, "w") as filename:
            manifest = {
                'metadata': {
                    'name': self.id.name,
                    'category': self.id.category,
                    'version': self.id.version,
                    'description': self.description,
                    'created_at': datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
                },
                'dependencies': self.run_dependencies,
            }
            toml.dump(manifest, filename)

    def __str__(self):
        return str(self.id)
