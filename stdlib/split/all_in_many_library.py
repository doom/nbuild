#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import stdlib
import glob
import os
from core.log import ilog
from core.args import get_args


def _find_all_libs_name() -> [(str, str)]:
    build = stdlib.current_build()

    libs = []

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
            raise RuntimeError("all_in_many_library() couldn't find any library in {,usr/}lib{,32,64}/")

        # Remove duplicate, if any
        libs = list(set(libs))

        # Generate both lib name and package name
        splits = map(lambda path: os.path.basename(path).split('.so.'), libs)
        libs = list(map(lambda splits: (splits[0].split('lib')[1], f'{splits[0]}{splits[1]}'), splits))

    return libs


def all_in_many_library() -> stdlib.Aggregate:
    ilog("Splitting using the \"All in many (library)\" method", indent=False)

    aggregate = stdlib.Aggregate()
    build = stdlib.current_build()
    libs = _find_all_libs_name()

    for (libname, so_name) in libs:
        # Create lib package
        lib = stdlib.Package(
            stdlib.PackageId(name=so_name),
            f'The {libname} library.',
            build.manifest.maintainer,
            build.manifest.licenses,
            build.manifest.upstream_url,
        )

        lib.drain(
            f'{{,usr/}}lib{{,32,64}}/lib{libname}.so.*',
            f'{{,usr/}}lib{{,32,64}}/pkgconfig/{{,lib}}{libname}{{/,.pc}}',
        )

        # Create dev package
        dev = stdlib.Package(
            stdlib.PackageId(name=f'{so_name}-dev'),
            f'Headers and manuals to write software using the {libname} library.',
            build.manifest.maintainer,
            build.manifest.licenses,
            build.manifest.upstream_url,
        )

        dev.drain(
            f'usr/include/{{,lib}}{libname}{{/,.h}}',
            f'{{,usr/}}lib{{,32,64}}/lib{libname}.{{a,so}}',
        )

        dev.depends_on(lib)

        # Create doc package
        doc = stdlib.Package(
            stdlib.PackageId(name=f'{so_name}-doc'),
            f'Documentation for the {libname} library.',
            build.manifest.maintainer,
            build.manifest.licenses,
            build.manifest.upstream_url,
        )

        doc.drain(
            f'usr/share/doc/{{lib,}}{libname}/',
            f'usr/share/info/{{lib,}}{libname}/',
        )

        doc.depends_on(lib)

        aggregate.push(lib, dev, doc)

    return aggregate
