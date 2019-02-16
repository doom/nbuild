#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from enum import Enum


class Arch(Enum):
    X86_64 = 'x86_64'
    X86 = 'x86'
    ARM = 'arm'
    ARM64 = 'arm64'
