import enum
from nbuild.log import ilog, qlog, wlog
import nbuild.checks.edit as edit


class Type(enum.Enum):
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()


class Check():
    global_state = Type.EDIT

    @staticmethod
    def commit(pkg):
        ilog("Recreating tarball")
        pkg.create_tarball()

    def __init__(self, items):
        self.items = items
        self.fails = []

    def run(self):
        for item in self.items:
            if not self.validate(item):
                self.fails.append(item)
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
    def __init__(self, pkg):
        super().__init__([pkg])

    @staticmethod
    def commit(pkg):
        ilog("Recreating manifest.toml")
        pkg.create_manifest()
