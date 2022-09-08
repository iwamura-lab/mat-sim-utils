import click

from ganson_utils.structure import convert_lammps_structure_to_poscar_by_ase


@click.command()
@click.option("--lammps_structure", required=True, help="lammps-data filename")
@click.option("--poscar_filename", required=True, help="POSCAR filename")
def main(lammps_structure, poscar_filename):
    symbol_of_each_type = {1: "Fe", 2: "Fe"}
    convert_lammps_structure_to_poscar_by_ase(
        lammps_structure_file=lammps_structure,
        poscar_structure_file=poscar_filename,
        symbol_of_each_type=symbol_of_each_type,
    )
