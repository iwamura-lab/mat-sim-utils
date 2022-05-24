from pathlib import Path

import pytest
from pymatgen.analysis.structure_matcher import StructureMatcher

test_dir_path = Path(__file__).resolve().parent


@pytest.fixture()
def inputs_dir_path():
    return test_dir_path / "data" / "inputs"


@pytest.fixture()
def outputs_dir_path():
    return test_dir_path / "data" / "outputs"


@pytest.fixture()
def structure_matcher():
    matcher = StructureMatcher(ltol=1e-5, stol=1e-5, primitive_cell=False, scale=False)
    return matcher
