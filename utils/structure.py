from typing import Dict

from ase.io import read
from pymatgen.core.periodic_table import Element


def convert_lammps_structure_to_poscar_by_ase(
    lammps_structure_file: str,
    poscar_structure_file: str,
    symbol_of_each_type: Dict[int, str] = None,
) -> None:
    """Convert lammps structure file to POSCAR format

    Args:
        lammps_structure_file (str): lammps-data format structure filename
        poscar_structure_file (str): poscar format structure filename
        symbol_of_each_type (Dict[int, str], optional): The element symbol of each type
            in original lammps structure. Defaults to None.
    """
    if symbol_of_each_type is None:
        z_of_type = None
    else:
        z_of_type = {}
        for atomic_type in symbol_of_each_type.keys():
            element = Element(symbol_of_each_type[atomic_type])
            z_of_type[atomic_type] = element.Z

    atoms = read(
        lammps_structure_file, format="lammps-data", Z_of_type=z_of_type, style="atomic"
    )
    atoms.write(poscar_structure_file, format="vasp")
