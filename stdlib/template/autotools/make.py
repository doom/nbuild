#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import stdlib


def make(
    *args,
    target='',
    binary='make',
    folder='.',
    fail_ok=False,
):
    stdlib.cmd(f'''{binary} -C {folder} {target} {' '.join(args)}''', fail_ok=fail_ok)
