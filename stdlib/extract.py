#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import tarfile
import shutil
import stdlib
import glob
from core.log import ilog, clog


def extract_tarballs(
    *files,
    move_subdir=True,
    subdir=None,
):
    build = stdlib.current_build()

    if len(files) == 0:
        files = glob.glob(f'{build.download_cache}/*.tar*')

    for tarball_path in files:
        ilog(f"Extracting {os.path.basename(tarball_path)}")
        with tarfile.open(tarball_path) as tar:
            tar.extractall(path=build.build_cache)

        # If sources are contained in a sub directory,
        # move the content one folder up
        if move_subdir:
            # Guess the name of the subdir
            if subdir is None:
                subdir = os.path.join(
                    build.build_cache,
                    os.path.basename(tarball_path).split('.tar')[0],
                )

            if os.path.exists(subdir):
                for filename in os.listdir(subdir):
                    shutil.move(
                        os.path.join(subdir, filename),
                        build.build_cache,
                    )

        clog(f"Extracted in {build.build_cache}")
