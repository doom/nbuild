#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from enum import Enum


class License(Enum):
    GPL_V1 = 'GPL v1'
    GPL_V2 = 'GPL v2'
    GPL_V3 = 'GPL v3'
    AGPL_V3 = 'AGPL v3'
    LGPL_V3 = 'LGPL v3'
    BSD = 'BSD'
    MOZILLA = 'MPL'
    MIT = 'MIT'
    APACHE = 'Apache'
    PUBLIC_DOMAIN = 'Public Domain'

    CUSTOM = 'Custom'
    NONE = 'None',
