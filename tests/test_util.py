from pypacter.util import get_version


def test_get_version() -> None:
    version = get_version()
    assert 3 <= len(version.split(".")) <= 5
