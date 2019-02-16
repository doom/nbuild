#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import stdlib
from glob import glob
from core.log import clog


def apply_patches(
    patches=None,
):
    build = stdlib.current_build()

    if patches is None:
        patches = glob(f'{build.download_cache}/*.patch')

    for patch_path in patches:
        stdlib.cmd(f'patch -Np1 -i {patch_path}')
        clog(f"Applied patch {os.path.basename(patch_path)}")
