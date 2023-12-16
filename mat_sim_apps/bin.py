import multiprocessing
from subprocess import run


def run_vasp() -> None:
    """Run VASP"""
    run(["cp", "POSCAR", "POSCAR.init"])

    n_core = multiprocessing.cpu_count()
    vasp_command = ["mpirun", "-np", str(n_core), "/usr/local/calc/vasp/vasp544mpi"]
    run(vasp_command)
