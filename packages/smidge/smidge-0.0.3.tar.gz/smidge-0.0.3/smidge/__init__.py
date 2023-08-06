from .itermixin import itermixin

class set(__builtins__['set'], itermixin):
    '''
    set() -> new empty set
    set(*iterable) -> new set of many items
    set(item) -> new set of 1 item
    set(item1, item2, item3) -> new set of 3 items

    Build a collection of unique elements.
    '''
    def __init__(set, *params):
        super().__init__(params)
