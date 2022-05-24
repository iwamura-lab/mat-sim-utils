from lammps_api.utils import convert_lammps_structure_to_poscar
from pymatgen.io.vasp import Poscar

from utils.structure import convert_lammps_structure_to_poscar_by_ase

test_structure_ids = ["042", "049", "091"]


def test_convert_lammps_structure_to_poscar(
    structure_matcher, inputs_dir_path, outputs_dir_path
):
    # Dump POSCARs
    for structure_id in test_structure_ids:
        structure_file_path = (
            inputs_dir_path / "Fe" / "structures" / f"structure-{structure_id}"
        )

        # Generate new structure files by structure_converter
        poscar_file_path = (
            outputs_dir_path / "structure_converter" / f"poscar-{structure_id}"
        )
        symbol_of_each_type = {1: "Fe", 2: "Fe"}
        convert_lammps_structure_to_poscar_by_ase(
            lammps_structure_file=str(structure_file_path),
            poscar_structure_file=str(poscar_file_path),
            symbol_of_each_type=symbol_of_each_type,
        )

        # Generate new structure files by seko's program
        poscar_file_path = outputs_dir_path / "seko" / f"poscar-{structure_id}"
        convert_lammps_structure_to_poscar(
            lammps_structure_file=str(structure_file_path),
            poscar_structure_file=str(poscar_file_path),
        )

    # Load generated POSCARs
    structure_converter_poscars = [
        Poscar.from_file(
            "/".join(
                [str(outputs_dir_path), "structure_converter", f"poscar-{structure_id}"]
            )
        )
        for structure_id in test_structure_ids
    ]
    seko_poscars = [
        Poscar.from_file(
            "/".join([str(outputs_dir_path), "seko", f"poscar-{structure_id}"])
        )
        for structure_id in test_structure_ids
    ]

    # Test if two structures are same
    for poscar1, poscar2 in zip(structure_converter_poscars, seko_poscars):
        assert structure_matcher.fit(poscar1.structure, poscar2.structure)
