class Error(Exception):
    pass


class DuplicateIdError(Error):
    """ Raised when the uniqueness constraint on id is violated. """
    pass


class NoIdError(Error):
    """ Raised when a namedtuple lacs an id field. """


class NoSuchIdError(Error):
    """ Raised when the specified id does not exist. """
