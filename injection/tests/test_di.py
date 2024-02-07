from src.injection.di import foo


class TestInjectionDi:
    def test_di(self):
        assert foo() == 1