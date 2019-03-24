import enum


class Type(enum.Enum):
    SHOW = enum.auto()
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()


class Check():
    global_state = Type.SHOW

    def __init__(self, items, local_state=None):
        self.items = items
        self.state = local_state
        self.fails = []

    def run(self):
        for item in self.items:
            if not self.validate(item):
                self.fails.append(item)
                s = self.state or Check.global_state
                if s is Type.SHOW:
                    self.show(item)
                elif s is Type.FIX:
                    self.fix(item)
                elif s is Type.DIFF:
                    self.diff(item)
                elif s is Type.EDIT:
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
