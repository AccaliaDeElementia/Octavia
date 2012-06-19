#!/usr/bin/python

# Behold, the great Decepticon: DOCUMENTATOR!

from inspect import getargspec 
from decorator import decorator

NoneType = type(None)

class DocumentatorError (Exception): pass

class Method(object):
    def __init__(self, func):
        helpstr = func.__doc__
        name = func.__name__
        params, _x, _y, defaults = getargspec(func)
        for name, value in locals().items():
            if name[0] != '_' :
                setattr(self, name, value)

    def dict(self):
        params = len(self.params)
        defaults = 0
        defd = []
        if self.defaults:
            defaults = len(self.defaults)
            defd = ['[%s]'%s for s in self.params[-defaults:]]
        parameters = self.params[:params-defaults] + defd
        return {
            'name': self.func.__name__, 
            'description': self.func.__doc__,
            'params': parameters
        }

__methods = {}

def registerMethod(func):
    __methods[func.__name__] = Method(func)
    return func

def help(method = None):
    if method is None:
        return [s.dict() for s in sorted(__methods.values(), key=lambda x: x.name)]
    return __methods[method].dict()
