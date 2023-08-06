class itermixin:
    '''
    Can be added as a superclass to iterables
    to gain its methods.
    '''
    def one(iterable):
        '''Converts an iterable of one item into its item,
        enforcing that the length must be one.

        First tries calling len(), then tries iterating to detect extra items.
        Builtin iterables often have a fast member variable for their length.

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
            # otherwise we can iterate to find out
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
