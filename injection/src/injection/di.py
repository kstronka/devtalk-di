from typing import TypeVar

T = TypeVar('T')

_registry = {}


def get_from_registry(interface: type) -> type:
    return _registry[interface]


def implements(*, interface: type):
    def decorator(impl: type):
        _registry[interface] = impl
        return impl

    return decorator

