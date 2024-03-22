import tempfile

import pytest

from cadet import Cadet


@pytest.fixture
def temp_cadet_file():
    """
    Create a new Cadet object for use in tests.
    """
    model = Cadet()

    with tempfile.NamedTemporaryFile() as temp:
        model.filename = temp
        yield model


def test_duplicate_keys(temp_cadet_file):
    """
    Test that the Cadet class raises a KeyError exception when duplicate keys are set on it.
    """
    with pytest.raises(KeyError):
        temp_cadet_file.root.input.foo = 1
        temp_cadet_file.root.input.Foo = 1

        temp_cadet_file.save()


if __name__ == "__main__":
    pytest.main()
