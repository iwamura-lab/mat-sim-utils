import re
from pathlib import Path
from subprocess import run

import click
from pymatgen.io.vasp import Vasprun


def extract_vasprun_id(filename: str) -> int:
    """Extract vasprun_id from the filename of vasprun.xml

    Args:
        filename (str): The filename of a vasprun.xml.

    Returns:
        int: vasprun_id.
    """
    vasprun_xml_pattern = re.compile(r"vasprun_(\d+).xml")
    m = vasprun_xml_pattern.search(filename)
    assert m is not None
    return int(m.group(1))


@click.command()
@click.option(
    "--n_core", default="16", show_default=True, help="The number of CPU cores."
)
@click.option("--run_static/--no-run_static", default=False, show_default=True)
def main(n_core, run_static) -> None:  # noqa: CCR001
    max_iterations = 10
    vasp_command = ["mpirun", "-np", n_core, "/usr/local/calc/vasp/vasp544mpi"]

    if run_static:
        if Path("KPOINTS-relax").exists():
            run(["cp", "KPOINTS-relax", "KPOINTS"])
        run(["cp", "INCAR-relax", "INCAR"])

    # Find the IDs of vasprun.xml in the current directory
    vasprun_id_list = [
        extract_vasprun_id(path.name) for path in Path.cwd().glob("vasprun_*.xml")
    ]
    vasprun_id_list.sort()

    # Calculate the number which vasprun_id begins with
    vasprun_id_begin = 1 if len(vasprun_id_list) == 0 else vasprun_id_list[-1] + 1

    if len(vasprun_id_list) == 0:
        run(["cp", "POSCAR", "POSCAR.init"])

    # Run Vasp at least once and continue until convergence
    converged = False
    for i in range(max_iterations):
        run(vasp_command)

        vasprun_id = str(vasprun_id_begin + i).zfill(2)
        run(["cp", "CONTCAR", "POSCAR"])
        run(["cp", "CONTCAR", f"CONTCAR_{vasprun_id}"])

        run(["cp", "vasprun.xml", f"vasprun_{vasprun_id}.xml"])

        vasprun = Vasprun(
            "vasprun.xml", parse_dos=False, parse_eigen=False, parse_potcar_file=False
        )
        if (i >= 1) and vasprun.converged_ionic:
            converged = True
            break

    if run_static and converged:
        if Path("KPOINTS-final").exists():
            run(["cp", "KPOINTS-final", "KPOINTS"])
        run(["cp", "INCAR-final", "INCAR"])
        run(vasp_command)

    # Output a log if relaxation doesn't converge in max_iterations run
    if not converged:
        with open("fail.log", "w") as f:
            f.write("Relaxation failed.")
