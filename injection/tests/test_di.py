from typing import Protocol

from src.injection.di import get_from_registry, implements, Require, override


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

    def test_require_always_get_implementation(self):
        @implements(interface=SimpleProtocol)
        class Echo:
            def echo(self, message: str):
                return message

        class Container:
            dep: SimpleProtocol = Require(SimpleProtocol)

        assert isinstance(Container.dep, Echo)

    def test_require_always_behaves_okay(self):
        @implements(interface=SimpleProtocol)
        class Echo:
            def echo(self, message: str):
                return message

        class Container:
            dep: SimpleProtocol = Require(SimpleProtocol)

        assert Container.dep.echo("hello") == "hello"

    def test_override_always_replaces_impl(self, mocker):
        @implements(interface=SimpleProtocol)
        class Echo:
            def echo(self, message: str):
                return message

        class Container:
            dep: SimpleProtocol = Require(SimpleProtocol)

        spy = mocker.MagicMock()

        with override(SimpleProtocol, using=spy):
            Container.dep.echo("hello")

        spy.echo.assert_called_once_with("hello")



