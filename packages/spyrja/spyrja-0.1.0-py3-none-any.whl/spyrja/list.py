from spyrja.common import Queryable


class List(Queryable):
    def __init__(self):
        super().__init__(list())

    def add(self, tuple):
        self.collection.append(tuple)
        return tuple

    def update(self, new_fields, **kwargs):
        new_collection = list()
        old_values = list()
        for t in self.collection:
            if List.is_match(t, kwargs):
                new_collection.append(t._replace(**new_fields))
                old_values.append(t)
            else:
                new_collection.append(t)
        self.collection = new_collection
        return old_values
