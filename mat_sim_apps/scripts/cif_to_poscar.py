from pathlib import Path

import click
from pymatgen.io.cif import CifParser
from pymatgen.io.vasp import Poscar


@click.command()
@click.option("-i", "--input_file", help="Path to a CIF file.")
@click.option("-o", "--output_file", help="Path to a new POSCAR.")
def main(input_file, output_file) -> None:
    """Convert a CIF file to a POSCAR"""
    # Convert CIF data to POSCAR data
    parser = CifParser(input_file, check_cif=False)
    structure = parser.parse_structures(primitive=False)[0]
    poscar = Poscar(structure)

    output_file_path = Path(output_file)
    if not output_file_path.parent.exists():
        output_file_path.parent.mkdir(parents=True)

    # Write the content of a new POSCAR
    content = poscar.get_str(significant_figures=16)
    with output_file_path.open("w") as f:
        f.write(content)
