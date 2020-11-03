"""`q` for `q`uick class definitions!  In the spirit of cluegen, but with no need of annotations.

class Point(q):
    x, y

This is all you need to get the __init__ and __repr__ one expects.
"""
from inspect import getsource
from sys import modules
from types import FunctionType


NO_DEFAULT = object()

def is_default(f):
    """If a value is a FunctionType, we check if it's not a lambda expression:  We'll assume lambda expressions in the class body
       are meant to be default values in the constructor.
    """
    if isinstance(f, FunctionType):
        *_, code = getsource(f).partition('=')
        return True if code.strip().startswith('lambda') else False
    return True

def lambda_source(f):
    """We can use a lambda's repr as a default value in the __init__, so we use getsource to reproduce the code.
    """
    *_, c = getsource(f).partition('=')
    return c.strip()


class AutoDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().__setitem__('__auto_attrs__', {})

    def __missing__(self, key):
        if key.startswith('__'):
            raise KeyError(key)

        if hasattr(modules[self['__module__']], key):
            return getattr(modules[self['__module__']], key)

        self['__auto_attrs__'][key] = NO_DEFAULT

    def __setitem__(self, key, val):
        if not key.startswith('__') and is_default(val):
            self['__auto_attrs__'][key] = val
        else:
            super().__setitem__(key, val)


class qMeta(type):
    def __prepare__(name, bases):
        return AutoDict()


def all_attrs(cls):
    attrs = {}
    for c in reversed(cls.__mro__):
        attrs.update(getattr(c, '__auto_attrs__', {}))

    no_defaults = [k for k, v in attrs.items() if v is NO_DEFAULT]
    defaults = {k:v for k, v in attrs.items() if v is not NO_DEFAULT}
    return no_defaults, defaults


class q(metaclass=qMeta):
    def __init_subclass__(cls):
        no_defaults, defaults = all_attrs(cls)

        no_default_args = ', '.join(no_defaults)
        default_args = ', '.join(f'{name}=' + (f'{lambda_source(val)}' if isinstance(val, FunctionType) else f'{val!r}') for name, val in defaults.items())
        all_args = no_defaults + list(defaults)
        sep = ', ' if no_default_args and default_args else ''

        init_header = f'def __init__(self{", " if all_args else ""}{no_default_args}{sep}{default_args}):\n'
        init_body = '\n'.join(f'    self.{name}={name}' for name in all_args) if all_args else '    pass'

        repr_header = 'def __repr__(self):\n'
        repr_body = '    return f"{{type(self).__name__}}({})"'.format(', '.join(f'{name}={{self.{name}!r}}' for name in all_args))

        loc = {}
        exec(init_header + init_body, loc)
        exec(repr_header + repr_body, loc)
        cls.__init__ = loc['__init__']
        cls.__repr__ = loc['__repr__']
