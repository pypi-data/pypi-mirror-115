from spyrja.common import Queryable


class Set(Queryable):
    def __init__(self):
        super().__init__(set())

    def add(self, tuple):
        self.collection.add(tuple)
        return tuple

    def update(self, new_fields, **kwargs):
        new_collection = set()
        old_values = set()
        for t in self.collection:
            if Set.is_match(t, kwargs):
                new_collection.add(t._replace(**new_fields))
                old_values.add(t)
            else:
                new_collection.add(t)
        self.collection = new_collection
        return old_values
