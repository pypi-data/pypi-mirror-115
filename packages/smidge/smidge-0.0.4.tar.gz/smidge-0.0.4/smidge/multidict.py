from collections import defaultdict
from smidge import set
from smidge import itermethods
from smidge.readonly import const

# todo? a nice slicing, ellipsis, or kwparams
#       syntax to access values in multiple ways
#       with one method.
class multidict(defaultdict):
    '''
        -> new dictionary object

        A multidict is a key-value mapping where
        each key can map to multiple values.

        Parameters:
            mapping_or_iterable:
                An optional object to take initial (key,value) tuples from.
            default_factory:
                A container to use for multiple values.
            mapping:
                Optional key=value pairs to add.
                If the type of a value is default_factory, it will be expanded.
    '''
    def __init__(self, mapping_or_iterable = (), default_factory = set, **mapping):
        super().__init__(default_factory)
        try:
            mapping_or_iterable = mapping_or_iterable.items()
        except:
            pass
        for key, value in mapping_or_iterable:
            self.add(key, value)
        for key, value in mapping.items():
            if type(value) is default_factory:
                self.add(key, *value)
            else:
                self.add(key, value)
    @const
    def all(self, key):
        '''Return the container of all items matching the given key.'''
        return self[key]
    @const
    def one(self, key):
        '''Return the single item matching a given key.

        Raises KeyError if there is not a unique item matching the key.
        '''
        return itermethods.one(self.all(key))
    @const
    def first(self, key):
        '''Return one item that matches the given key.

        Raises KeyError if no items match.
        '''
        return itermethods.first(self.all(key))
    @const
    def len(self, key):
        '''Returns the number of items matching the given key.'''
        return len(self.all(key))
    def add(self, key, *values):
        '''Adds values to a key in the multidict.'''
        container = self.all(key)
        for value in values:
            container.add(value)
    def discard(self, key, *values):
        '''Removes values from the multidict.'''
        oldset = self.all(key)
        for value in values:
            oldset.discard(value)
        # delete if set is now empty
        for item in oldset:
            return
        del self[key]
    def move(self, oldkey, newkey, *values):
        '''Changes the key associated with values.

        None may be provided for a key, to create or remove values with generic code.'''
        if oldkey != newkey:
            if oldkey is not None:
                self.discard(oldkey, *values)
            if newkey is not None:
                self.add(newkey, *values)
    @const
    def values(self):
        for container in super().values():
            yield from container
    @const
    def __len__(self):
        sum = 0
        for container in super().values():
            sum += len(container)
        return sum
    def __missing__(self, key):
        value = self.default_factory()
        super().__setitem__(key, value)
        return value
    def __setitem__(self, key, value):
        container = self.all(key)
        if type(value) is type(container):
            container.clear()
            container.update(value)
        else:
            if itermethods.is_many(container):
                raise KeyError('multiple items')
            container.clear()
            container.add(value)
