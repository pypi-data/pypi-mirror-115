def remove(collection, **fields):
    try:
        # Is this a dictionary?
        collection.keys()
        return ((k, v) for k, v in collection.items()
                if not is_match(v, fields))
    except AttributeError:
        # No, it's an iterable
        return (e for e in collection if not is_match(e, fields))


def update(collection, new_fields, **fields):
    try:
        # Is this a dictionary?
        collection.keys()
        for k, t in collection.items():
            if is_match(t, fields):
                yield (k, t._replace(**new_fields))
            else:
                yield (k, t)
    except AttributeError:
        # No, it's an iterable
        for t in collection:
            if is_match(t, fields):
                yield t._replace(**new_fields)
            else:
                yield t


def get(collection, **fields):
    try:
        # Is this a dictionary?
        collection.keys()
        return ((k, v) for k, v in collection.items() if is_match(v, fields))
    except AttributeError:
        # No, it's an iterable
        return (e for e in collection if is_match(e, fields))


def is_match(t, fields):
    for k, v in fields.items():
        try:
            tv = getattr(t, k)
            # Is this a function?
            if not v(tv):
                return False
        except TypeError:
            # No,it's a value
            if tv != v:
                return False
        except AttributeError:
            # This tuple doesn't have this field
            return False
    return True
