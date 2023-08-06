from spyrja.common import Queryable


class Set(Queryable):
    def __init__(self):
        super().__init__(set())

    def add(self, tuple):
        self.collection.add(tuple)
        return tuple
