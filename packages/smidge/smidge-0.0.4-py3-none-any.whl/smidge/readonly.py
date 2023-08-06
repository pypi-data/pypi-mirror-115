class readonly:
    '''Wraps a container, implying that
       access is read-only.

       The container is proxied, with
       the exception that callable attributes
       are only visible if their names contain
       the string 'get' or they are annotated
       with '@const'.
       '''
    def __init__(self, container):
        self._container = container
    def __getattr__(self, attr):
        val = getattr(self._container, attr)
        if not callable(val):
            return val
        if hasattr(val, '__const') or 'get' in attr:
            setattr(self, attr, val)
            return val
        raise AttributeError(attr)
    def __getitem__(self, item):
        return self._container[item]
    def __iter__(self):
        return iter(self._container)

def const(method):
    '''A decorator that will tell readonly the method is safe.'''
    method.__const = True
    return method
