#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import core
import stdlib
import stdlib.build
from core.log import clog, wlog


class Manifest():
    def __init__(
        self,
        path: str,
        name: str,
        category: str,
        description: str,
        maintainer: str,
        licenses: [stdlib.License],
        upstream_url: str,
        versions_data: [],
        build_deps=[]
    ):
        self.path = path
        self.name = name
        self.category = category
        self.description = description.replace('\n', ' ').strip()
        self.maintainer = maintainer
        self.licenses = licenses
        self.upstream_url = upstream_url
        self.versions_data = versions_data
        self.build_deps = build_deps


def manifest(**kwargs):
    def exec_manifest(builder):
        m = Manifest(
            path=os.path.join(
                os.getcwd(),
                core.args.get_args().manifest,  # Safe because only one manifest is given to nbuild
            ),
            **kwargs
        )

        # Install build dependencies
        for build_dep in m.build_deps:
            clog(f"Installing build depn \"{build_dep}\"", indent=False)

        # Build all versions
        for version_data in m.versions_data:
            build = stdlib.Build(m, version_data)
            stdlib.build._set_current_build(build)

            # Save state before executing the manifest
            with stdlib.pushd(build.build_cache):
                with stdlib.pushenv():
                    clog(f"Building {build}", indent=False)
                    pkgs_iterator = builder(build)

                    if build.is_empty():
                        clog("No leftovers files in the build directory.", indent=False)
                    else:
                        wlog("Some built files haven't been moved to any package:", indent=False)

                    # Warn if build has leftover files
                    build.warn_leftovers()

                    # Wrap packages
                    for pkg in pkgs_iterator:
                        if not pkg.is_empty():
                            pkg.wrap()
                        else:
                            wlog(f"{pkg} is empty, skipped!", indent=False)

    return exec_manifest
