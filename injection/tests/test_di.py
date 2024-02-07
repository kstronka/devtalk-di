from typing import Protocol

from src.injection.di import get_from_registry, implements


class SimpleProtocol(Protocol):
    def echo(self, message: str) -> str:
        ...


class TestInjectionDi:
    def test_implements_always_register_implementation_for_protocol(self):
        @implements(interface=SimpleProtocol)
        class Echo:
            def echo(self, message: str):
                return message

        assert issubclass(get_from_registry(SimpleProtocol), Echo)

