import click
from pymatgen.io.vasp import Poscar, Vasprun


@click.command()
@click.argument("vasprun_xml_file")
@click.option(
    "--magnetic/--no-magnetic",
    default=True,
    show_default=True,
    help="Whether the system is magnetic or not.",
)
def main(vasprun_xml_file, magnetic) -> None:
    """Reproduce POSCAR at the last ionic step from vasprun.xml"""
    vasprun = Vasprun(
        vasprun_xml_file, parse_dos=False, parse_eigen=False, parse_potcar_file=False
    )
    poscar = Poscar(vasprun.structures[-1])
    poscar.write_file("POSCAR", significant_figures=16)

    # Modify the element line in POSCAR
    if magnetic:
        with open("POSCAR") as f:
            poscar_lines = [line.strip() for line in f]

        element = poscar_lines[5]
        n_atom = int(poscar_lines[6])
        poscar_lines[5] = " ".join([element] * 2)
        poscar_lines[6] = " ".join([str(n_atom // 2)] * 2)

        with open("POSCAR", "w") as f:
            f.write("\n".join(poscar_lines))
