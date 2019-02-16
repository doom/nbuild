#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import subprocess
from copy import deepcopy
from textwrap import dedent
from core.args import get_args
from core.log import ilog, dlog, flog


def cmd(
    cmd,
    fail_ok=False,
):
    """
    Executes the given command, after removing any prior whitespaces with
    `textwrap.dedent()`.

    This is nothing more than a wrapper to reduce boilerplate.
    """

    cmd = dedent(cmd)

    #if get_args().verbose >= 1:
    #    ilog(cmd)
    #    dlog(f"Working directory: {os.getcwd()}")

    #    if nbuild_args.verbose >= 2:
    #        for (key, value) in new_env.items():
    #            dlog(f'    {key}={value}')

    #if nbuild_args.verbose >= 3:
    #    code = subprocess.run(
    #        ['bash', '-e', '-c', cmd],
    #        env=new_env
    #    ).returncode
    #else:
    #    code = subprocess.run(
    #        ['bash', '-e', '-c', cmd],
    #        env=new_env,
    #        stdout=subprocess.DEVNULL,
    #        stderr=subprocess.DEVNULL
    #    ).returncode

    code = subprocess.run(['bash', '-e', '-c', cmd]).returncode

    if code != 0 and not fail_ok:
        flog(f"Command failed with error code {code}:")
        dlog(f"Working directory: {os.getcwd()}")

        for (key, value) in os.environ.items():
            dlog(f'    {key}={value}')

        print(cmd)
        exit(1)
