class itermethods:
    '''
    Can be mixed in as a superclass to iterables
    to gain its methods.

    Conditions that depend on length first try
    calling len(), then try iterating to detect
    just enough items needed.  Builtin iterables
    often have a fast member variable for their
    length.
    '''
    def one(iterable):
        '''Converts an iterable of one item into its item,
        enforcing that the length must be one.

        Returns:
            Unwrapped item

        Raises:
            KeyError if the container is not of length 1
        '''
        try:
            if len(iterable) != 1:
                raise KeyError('not of length 1')
            for item in iterable:
                return item
        except TypeError:
            found = None
            for item in iterable:
                if found is not None:
                    raise KeyError('multiple items')
                found = item
            if found is None:
                raise KeyError('not found')
            return found
    def first(iterable):
        '''Retrieves the first item from iterating.

        Returns:
            First item found

        Raises:
            KeyError if the iterable is empty
        '''
        for item in iterable:
            return item
        raise KeyError('not found')
    def is_none(iterable):
        '''Returns True if the iterable is empty.'''
        try:
            return len(iterable) == 0
        except TypeError:
            for item in iterable:
                return True
            return False
    def is_one(iterable):
        '''Returns True if the iterable contains exactly 1 item.'''
        try:
            itermethods.one(iterable)
            return True
        except KeyError:
            return False
    def is_many(iterable):
        '''Returns True if the iterable contains more than 1 item.'''
        try:
            return len(iterable) > 1
        except TypeError:
            found = False
            for item in iterable:
                if found:
                    return True
                found = True
            return False
