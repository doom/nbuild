import enum
from nbuild.log import ilog


class Type(enum.Enum):
    SHOW = enum.auto()
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()


class Check():
    global_state = Type.SHOW

    @staticmethod
    def commit(pkg):
        ilog("Recreating tarball")
        pkg.create_tarball()

    def __init__(self, items, local_state=global_state):
        self.items = items
        self.state = local_state
        self.fails = []

    def run(self):
        for item in self.items:
            if not self.validate(item):
                self.fails.append(item)
                if self.state is Type.SHOW:
                    self.show(item)
                elif self.state is Type.FIX:
                    self.fix(item)
                elif self.state is Type.DIFF:
                    self.diff(item)
                elif self.state is Type.EDIT:
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
