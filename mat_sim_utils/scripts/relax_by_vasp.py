from subprocess import run

import click
from pymatgen.io.vasp import Vasprun


@click.command()
@click.option(
    "--n_core", default="16", show_default=True, help="The number of CPU cores."
)
@click.option("--run_static/--no-run_static", default=False, show_default=True)
def main(n_core, run_static) -> None:  # noqa: CCR001
    max_iterations = 10
    vasp_command = ["mpirun", "-np", n_core, "/usr/local/calc/vasp/vasp544mpi"]

    if run_static:
        run(["cp", "INCAR-relax", "INCAR"])
    run(["cp", "POSCAR", "POSCAR.init"])

    # Run Vasp at least once and continue until convergence
    converged = False
    for i in range(max_iterations):
        run(vasp_command)

        run(["cp", "CONTCAR", "POSCAR"])
        vasprun_id = str(i + 1).zfill(2)
        run(["cp", "vasprun.xml", f"vasprun_{vasprun_id}.xml"])

        vasprun = Vasprun(
            "vasprun.xml", parse_dos=False, parse_eigen=False, parse_potcar_file=False
        )
        if (i >= 1) and vasprun.converged_ionic:
            converged = True
            break

    if run_static and converged:
        run(["cp", "INCAR-final", "INCAR"])
        run(vasp_command)

    # Output a log if relaxation doesn't converge in max_iterations run
    if not converged:
        with open("fail.log", "w") as f:
            f.write("Relaxation failed.")
