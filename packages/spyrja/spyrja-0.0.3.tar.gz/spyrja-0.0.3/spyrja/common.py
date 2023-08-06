class Queryable:
    def __init__(self, collection):
        self.collection = collection

    def get(self, **kwargs):
        for e in self.collection:
            match = True
            for k, v in kwargs.items():
                try:
                    ev = getattr(e, k)
                    if not v(ev):
                        match = False
                        break
                except TypeError:
                    if ev != v:
                        match = False
                        break
                except AttributeError:
                    match = False
                    break
            if match:
                yield e

    def remove(self, **kwargs):
        to_remove = list(self.get(**kwargs))
        for t in to_remove:
            self.collection.remove(t)
        return to_remove
