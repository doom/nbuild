#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re
from nbuild.log import elog, ilog, clog, wlog
import nbuild.checks.base as base


class IdCheck(base.CheckOnManifest):
    def __init__(self, pkg, local_state=None):
        super().__init__(pkg, local_state=local_state)

    def validate(self, item):
        pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
        return pattern.match(item.id) is not None

    def show(self, item):
        elog(f"The ID {item.id} doesn't respect the required syntax.")


class DescriptionCheck(base.CheckOnManifest):
    def __init__(self, pkg, local_state=None):
        print(local_state)
        super().__init__(pkg, local_state=local_state)

    def validate(self, item):
        a = len(item.description) >= 2 \
                and item.description[0].isupper() \
                and item.description[-1] == '.'
        print(a)
        return a

    def show(self, item):
        elog(
            f"The description of the package {item.id} "
            "doesn't respect the required syntax."
        )

    def fix(self, item):
        if len(item.description) < 2:
            wlog("Nothing can be done automatically, the description is too short")
        else:
            if item.description[-1] != '.':
                item.description += '.'
            if not item.description[0].isupper():
                item.description = item.description[0].upper() + item.description[1:]


# def id_syntax_check(package):
#     ilog("Checking id")
#     pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
#     if pattern.match(package.id) is None:
#         elog(f"The ID {package.id} doesn't respect the required syntax.")
#         return False
#     return True
#
#
# def desc_syntax_check(package):
#     ilog("Checking description")
#     pattern = re.compile(r'^[A-Z].*\.$')
#     if pattern.match(package.description) is None:
#         elog(
#             f"The description of the package {package.id} "
#             "doesn't respect the required syntax."
#             )
#         return False
#     return True
#
#
# def check_syntax(pkg):
#     ret = all([
#         id_syntax_check(pkg),
#         desc_syntax_check(pkg),
#     ])
#     if ret:
#         clog("\tAll syntax checks OK")
#     else:
#         elog("\tSome syntax checks failed")
#     return ret
