#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re
from nbuild.log import elog, ilog, clog, wlog
import nbuild.checks.base as base


class IdCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        super().__init__(pkg)

    def validate(self, item):
        pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
        return pattern.match(item.id) is not None

    def show(self, item):
        elog(f"The ID {item.id} doesn't respect the required syntax.")


class DescriptionCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        super().__init__(pkg)

    def validate(self, item):
        return len(item.description) >= 2 \
                and item.description[0].isupper() \
                and item.description[-1] == '.'

    def show(self, item):
        elog(
            f"The description of the package {item.id} "
            "doesn't respect the required syntax"
        )

    def fix(self, item):
        if len(item.description) < 2:
            wlog("Nothing can be done automatically, the description is too short")
        else:
            if item.description[-1] != '.':
                item.description += '.'
            if not item.description[0].isupper():
                item.description = item.description[0].upper() + item.description[1:]
