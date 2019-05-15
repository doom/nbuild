#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import re
from stdlib.log import elog, ilog, slog, wlog
import stdlib.checks.base as base
import stdlib.checks.edit as edit
import os


class IdCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        super().__init__(pkg)

    def validate(self, item):
        pattern = re.compile(r'^[a-z\-]+::[a-z\-]+\/[a-z\-]+\d*#(?:\d+\.){2}\d+$')
        return pattern.match(item.id) is not None

    def show(self, item):
        elog(f"The ID {item.id} doesn't respect the required syntax.")

    def fix(self, item):
        wlog("Item ID cannot be automatically fixed")

    def diff(self, item):
        wlog("No change can be made automatically")

    def edit(self, item):
        toml_path = os.path.join(self.pkg.package_dir, 'manifest.toml')
        edit.open_editor(toml_path)


class DescriptionCheck(base.CheckOnManifest):
    def __init__(self, pkg):
        super().__init__(pkg)
        self.pkg = pkg
        self.capital = False
        self.full_stop = False

    def validate(self, item):
        self.capital = item.description[0].isupper()
        self.full_stop = item.description[-1] == '.'

        return len(item.description) >= 2 and self.capital and self.full_stop

    def show(self, item):
        elog(
            f"The description of the package {item.id} "
            "doesn't respect the required syntax"
        )

    def fix(self, item):
        if len(item.description) < 2:
            wlog("Nothing can be done automatically, the description is too short")
        else:
            if not self.full_stop:
                item.description += '.'
                ilog("Full stop has been added at the end")
            if not self.capital:
                item.description = item.description[0].upper() + item.description[1:]
                ilog("First letter has been converted to uppercase")
            base.CheckOnManifest.commit(self.pkg)

    def diff(self, item):
        if not self.capital:
            ilog("The first letter would be converted to uppercase")
        if not self.full_stop:
            ilog("A full stop would be added at the end")

    def edit(self, item):
        toml_path = os.path.join(self.pkg.package_dir, 'manifest.toml')
        edit.open_editor(toml_path)
