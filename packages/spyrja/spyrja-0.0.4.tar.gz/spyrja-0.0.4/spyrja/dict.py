from .common import Queryable


class Dict(Queryable):
    def __init__(self):
        super().__init__(dict())

    def __getitem__(self, key):
        return self.collection[key]

    def __setitem__(self, key, value):
        self.collection[key] = value

    def get(self, **kwargs):
        for k, v in self.collection.items():
            if Dict.is_match(v, kwargs):
                yield (k, v)

    def remove(self, **kwargs):
        to_remove = dict(self.get(**kwargs))
        for k in to_remove.keys():
            self.collection.pop(k)
        return to_remove
