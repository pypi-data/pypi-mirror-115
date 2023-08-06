class Queryable:
    def __init__(self, collection):
        self.collection = collection

    def get(self, **kwargs):
        return (e for e in self.collection if Queryable.is_match(e, kwargs))

    def is_match(t, fields):
        for k, v in fields.items():
            try:
                tv = getattr(t, k)
                if not v(tv):
                    return False
            except TypeError:
                if tv != v:
                    return False
            except AttributeError:
                return False
        return True

    def remove(self, **kwargs):
        to_remove = list(self.get(**kwargs))
        for t in to_remove:
            self.collection.remove(t)
        return to_remove
