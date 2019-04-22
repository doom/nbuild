import enum
from nbuild.log import ilog, qlog, wlog
import nbuild.checks.edit as edit


class Type(enum.Enum):
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()


class Check():
    global_state = None

    @staticmethod
    def commit(pkg):
        ilog("Recreating tarball")
        pkg.create_tarball()

    def __init__(self, items, local_state=None):
        self.items = items
        self.state = local_state or Check.global_state
        self.fails = []

    def run(self):
        for item in self.items:
            if not self.validate(item):
                self.fails.append(item)
                self.show(item)
                if self.state is Type.FIX:
                    self.fix(item)
                elif self.state is Type.DIFF:
                    self.diff(item)
                elif self.state is Type.EDIT:
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
