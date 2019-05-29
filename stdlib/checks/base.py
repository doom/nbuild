import enum
import os
import toml
import datetime
from stdlib.log import ilog, qlog, wlog
import stdlib.checks.edit as edit


class Type(enum.Enum):
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()


class Check():
    global_state = Type.EDIT

    def __init__(self, items):
        self.items = items

    def run(self):
        for item in self.items:
            if not self.validate(item):
                self.show(item)
                if Check.global_state is Type.FIX:
                    self.fix(item)
                elif Check.global_state is Type.DIFF:
                    self.diff(item)
                elif Check.global_state is Type.EDIT:
                    ilog("The automatic changes would be as follows")
                    self.diff(item)
                    answer = edit.ask("Accept those changes? ")
                    if answer is True:
                        self.fix(item)
                    elif answer == 'edit':
                        self.edit(item)

    def validate(self, item):
        raise NotImplementedError

    def show(self, item):
        raise NotImplementedError

    def fix(self, item):
        raise NotImplementedError

    def diff(self, item):
        raise NotImplementedError

    def edit(self, item):
        raise NotImplementedError


class CheckOnManifest(Check):
    def __init__(self, pkg, items):
        super().__init__(items)
        self.pkg = pkg
        self.manifest_path = os.path.join(self.pkg.wrap_cache, 'manifest.toml')
        self.manifest = toml.load(self.manifest_path)

    def edit(self, item):
        edit.open_editor(self.manifest_path)
        self.pkg.refresh_manifest_wrap_date(self.manifest_path)
        self.manifest = toml.load(self.manifest_path)

    def update_manifest(self):
        with open(self.manifest_path, 'w') as filename:
            toml.dump(self.manifest, filename)
