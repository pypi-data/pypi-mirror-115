from uuid import uuid4

from .list import List
from .errors import DuplicateIdError, NoIdError, NoSuchIdError


class IdList(List):
    def id(self):
        return uuid4()

    def add(self, tuple):
        try:
            next(self.get(id=tuple.id))
            raise DuplicateIdError
        except StopIteration:
            self.collection.append(tuple)
        except AttributeError:
            raise NoIdError
        return tuple

    def update(self, new_tuple):
        try:
            [tuple] = list(self.get(id=new_tuple.id))
        except ValueError:
            raise NoSuchIdError
        except AttributeError:
            raise NoIdError
        self.collection[self.collection.index(tuple)] = new_tuple
        return tuple
