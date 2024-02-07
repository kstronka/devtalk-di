from typing import TypeVar
from contextlib import contextmanager


_registry = {}


def get_from_registry(interface: type) -> type:
    return _registry[interface]


def implements(*, interface: type):
    def decorator(impl: type | object):
        _registry[interface] = impl
        return impl

    return decorator


class Require:
    def __init__(self, interface):
        self._interface = interface

    def __get__(self, instance, owner):
        maybe_cls = _registry[self._interface]

        if isinstance(maybe_cls, type):
            return maybe_cls()

        return maybe_cls


def require_kwargs(**deps):
    def get(interface):
        maybe_cls = _registry[interface]

        if isinstance(maybe_cls, type):
            return maybe_cls()

        return maybe_cls

    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **(kwargs | {k: get(i) for k, i in deps.items()}))

        return wrapper

    return decorator



@contextmanager
def override(interface: type, *, using):
    old = get_from_registry(interface)
    implements(interface=interface)(using)
    yield
    implements(interface=interface)(old)
