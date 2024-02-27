from pypacter_api import __version__


def test_version() -> None:
    assert len(__version__.split(".")) >= 3
