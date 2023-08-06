from smidge.itermethods import itermethods
from smidge.readonly import readonly, const # todo? const's object-labeling behavior could be generic

class set(__builtins__['set'], itermethods):
    '''
    set() -> new empty set
    set(*iterable) -> new set of many items
    set(item) -> new set of 1 item
    set(item1, item2, item3) -> new set of 3 items

    Build a collection of unique elements.
    '''
    def __init__(set, *params):
        super().__init__(params)

from smidge.multidict import multidict

