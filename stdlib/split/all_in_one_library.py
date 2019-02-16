#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import stdlib
import glob
import os
from core.log import ilog
from core.args import get_args


def _find_so_version() -> str:
    build = stdlib.current_build()
    so_ver = ''

    with stdlib.pushd(build.install_cache):
        libs = [] \
            + glob.glob('lib/*.so.[0-9]') \
            + glob.glob('lib64/*.so.[0-9]') \
            + glob.glob('lib32/*.so.[0-9]') \
            + glob.glob('usr/lib/*.so.[0-9]') \
            + glob.glob('usr/lib64/*.so.[0-9]') \
            + glob.glob('usr/lib32/*.so.[0-9]') \
            + glob.glob('usr/local/lib/*.so.[0-9]') \
            + glob.glob('usr/local/lib64/*.so.[0-9]') \
            + glob.glob('usr/local/lib32/*.so.[0-9]')

        if len(libs) == 0:
            raise RuntimeError("all_in_one_library() couldn't find any library in {,usr/}lib{,32,64}/")

        # Remove duplicate, if any
        libs = list(set(libs))

        libs = map(lambda path: os.path.basename(path), libs)

        # Ensure all libraries have same major SO version, throw error otherwise.
        so_ver = next(libs).split('.so.')[1]
        for lib in libs:
            new_ver = lib.split('.so.')[1]
            if new_ver != so_ver:
                raise RuntimeError(
                    "all_in_one_library() found two+ libraries with different SO version."
                    "You should probably specify the library version by hand or use all_in_many_library()."
                )

    return so_ver


def all_in_one_library(so_version=None) -> stdlib.Aggregate:
    build = stdlib.current_build()

    ilog("Splitting using the \"All in one (library)\" method", indent=False)

    # Create the library package
    if so_version is None:
        so_version = _find_so_version()
    name = build.manifest.name
    lib = stdlib.Package(
        stdlib.PackageId(
            name=f'lib{name}{so_version}',
        ),
        build.manifest.description,
        build.manifest.maintainer,
        build.manifest.licenses,
        build.manifest.upstream_url,
    )

    lib.drain(
        '{,usr/}lib{,32,64}/*.so.*',
        '{,usr/}lib{,32,64}/pkgconfig/',
        '{,usr/}lib{,32,64}/*.pc',
        'usr/share/man/man{4,5,7,8}/',
        'usr/share/locale/',
        'usr/libexec/',
        'etc/',
    )

    # Create the binary package
    bin = stdlib.Package(
        stdlib.PackageId(
            name=f'{name}{so_version}-bin',
            category='sys-bin',
        ),
        f'Binary and utilities related to the {build.manifest.name} library.',
        build.manifest.maintainer,
        build.manifest.licenses,
        build.manifest.upstream_url,
    )

    bin.move('usr/local/bin/*', 'usr/bin/')

    bin.drain(
        '{,usr/}{,s}bin/',
        'usr/share/man/man{1,6,9}/',
        'usr/share/{locale,bash-completion/completions}/',
    )

    bin.move('usr/local/bin/*', 'usr/bin/')
    bin.depends_on(lib)

    # Create dev package
    dev = stdlib.Package(
        stdlib.PackageId(
            name=f'lib{name}{so_version}-dev',
        ),
        f'Headers and manuals to write software using the {build.manifest.name} library.',
        build.manifest.maintainer,
        build.manifest.licenses,
        build.manifest.upstream_url,
    )

    dev.drain(
        'usr/include/',
        '{,usr/}lib{,32,64}/*.{a,so}',
        'usr/share/man/man{2,3}/',
    )

    dev.depends_on(lib)

    # Create doc package
    doc = stdlib.Package(
        stdlib.PackageId(
            name=f'lib{name}{so_version}-doc',
        ),
        f'Documentation for the {build.manifest.name} library.',
        build.manifest.maintainer,
        build.manifest.licenses,
        build.manifest.upstream_url,
    )

    doc.drain(
        'usr/share/doc/',
        'usr/share/info/',
    )

    return stdlib.Aggregate(lib, bin, dev, doc)
