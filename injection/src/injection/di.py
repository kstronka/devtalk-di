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


@contextmanager
def override(interface: type, *, using):
    old = get_from_registry(interface)
    implements(interface=interface)(using)
    yield
    implements(interface=interface)(old)
