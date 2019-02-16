#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os
import stdlib


def configure(
    *flags,
    common_flags=True,
    binary='../configure',
    prefix='/usr',
    bindir='/usr/bin',
    sbindir='/usr/bin',
    libdir='/usr/lib64',
    libexecdir='/usr/libexec',
    includedir='/usr/include',
    datarootdir='/usr/share',
    datadir='/usr/share',
    infodir='/usr/share/info',
    mandir='/usr/share/man',
    sysconfdir='/etc',
    localstatedir='/var',
):
    if common_flags:
        _cmn_flags = f''' \
            --build="{os.environ['TARGET']}" \
            --host="{os.environ['HOST']}" \
            \
            --disable-option-checking \
            \
            --prefix="{prefix}" \
            --bindir="{bindir}" \
            --sbindir="{sbindir}" \
            --libdir="{libdir}" \
            --libexecdir="{libexecdir}" \
            --includedir="{includedir}" \
            --datarootdir="{datarootdir}" \
            --datadir="{datadir}" \
            --infodir="{infodir}" \
            --mandir="{mandir}" \
            --sysconfdir="{sysconfdir}" \
            --localstatedir="{localstatedir}" \
            \
            --enable-shared \
            --enable-static \
            --with-shared \
            --with-static \
            \
            --enable-stack-protector=all \
            --enable-stackguard-randomization \
            --disable-werror \
            \
            --with-packager='Raven-OS' \
            --with-bugurl='https://bugs.raven-os.org' \
        '''
    else:
        _cmn_flags = ''

    stdlib.cmd(f''' \
        {binary} \
            {_cmn_flags} \
            {' '.join(flags)}
        ''')
