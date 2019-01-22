
def get_descendents(cls, filtered_by: set = {}):
    """
    Given a Class cls, find and return a list of its descendents classes, which are not included in filtered_by
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_descendents(c)]) - set(filtered_by)
