import multiprocessing
from pathlib import Path
from subprocess import run

from pymatgen.io.vasp import Vasprun

from mat_sim_apps.utils import extract_vasprun_id


def run_vasp() -> None:
    """Run VASP"""
    run(["cp", "POSCAR", "POSCAR.init"])

    n_core = multiprocessing.cpu_count()
    vasp_command = ["mpirun", "-np", str(n_core), "/usr/local/calc/vasp/vasp544mpi"]
    run(vasp_command)


# flake8: noqa: CCR001
def relax_by_vasp(
    incar_relax: str = "INCAR-relax",
    run_static: bool = False,
) -> None:
    n_core = multiprocessing.cpu_count()
    max_iterations = 10
    vasp_command = ["mpirun", "-np", str(n_core), "/usr/local/calc/vasp/vasp544mpi"]

    if run_static:
        if Path("KPOINTS-relax").exists():
            run(["cp", "KPOINTS-relax", "KPOINTS"])
        run(["cp", incar_relax, "INCAR"])

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
            print("Relaxation failed.", file=f)
