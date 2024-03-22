import tempfile

import numpy as np
import pytest
from addict import Dict

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


def test_save_as_python(temp_cadet_file):
    """
    Test that the Cadet class raises a KeyError exception when duplicate keys are set on it.
    """
    # initialize "sim" variable to be overwritten by the exec lines later
    sim = Cadet()

    # Populate temp_cadet_file with all tricky cases currently known
    temp_cadet_file.root.input.foo = 1
    temp_cadet_file.root.input.bar.baryon = np.arange(10)
    temp_cadet_file.root.input.bar.barometer = np.linspace(0, 10, 9)
    temp_cadet_file.root.input.bar.init_q = np.array([], dtype=np.float64)
    temp_cadet_file.root.input["return"].split_foobar = 1

    code_lines = temp_cadet_file.save_as_python_script(filename="temp.py", only_return_pythonic_representation=True)

    # remove code lines that save the file
    code_lines = code_lines[:-2]

    # populate "sim" variable using the generated code lines
    for line in code_lines:
        exec(line)

    # test that "sim" is equal to "temp_cadet_file"
    recursive_equality_check(sim.root, temp_cadet_file.root)


def recursive_equality_check(dict_a: dict, dict_b: dict):
    assert dict_a.keys() == dict_b.keys()
    for key in dict_a.keys():
        value_a = dict_a[key]
        value_b = dict_b[key]
        if type(value_a) in (dict, Dict):
            recursive_equality_check(value_a, value_b)
        elif type(value_a) == np.ndarray:
            np.testing.assert_array_equal(value_a, value_b)
        else:
            assert value_a == value_b
    return True


if __name__ == "__main__":
    pytest.main()
