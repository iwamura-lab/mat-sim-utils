import multiprocessing
import re
import shutil
from pathlib import Path
from subprocess import run

from pymatgen.io.vasp import Vasprun

from mat_sim_apps.structure import refine_poscar_file
from mat_sim_apps.utils import extract_vasprun_id


def check_std_log() -> str:
    """Check std.log in current directory

    Returns:
        str: The status code based on std.log.
    """
    std_log_bak_path = Path("std.log.bak")
    if std_log_bak_path.is_file():
        with std_log_bak_path.open("r") as f:
            begin_lid = len(f.readlines())
    else:
        begin_lid = 0

    band_crossing_pattern = re.compile(r".*band-crossing.*")
    error_pattern = re.compile(r".*error.*", re.IGNORECASE)
    warning_pattern = re.compile(r".*warning.*", re.IGNORECASE)

    with open("std.log") as f:
        lines = [line.strip() for line in f]
    status_code = "SUCCESS"
    for line in lines[begin_lid:]:
        if band_crossing_pattern.match(line):
            status_code = "NBANDS"
            break
        if error_pattern.match(line):
            status_code = "ERROR"
        if warning_pattern.match(line):
            status_code = "WARNING"

    return status_code


def run_vasp() -> str:
    """Run VASP

    Returns:
        str: The status code.
    """
    poscar_path = Path.cwd() / "POSCAR"
    poscar_init_path = Path.cwd() / "POSCAR.init"
    if poscar_init_path.exists():
        shutil.copyfile(poscar_init_path, poscar_path)
    else:
        shutil.copyfile(poscar_path, poscar_init_path)

    n_core = multiprocessing.cpu_count()
    vasp_command = ["mpirun", "-np", str(n_core), "/usr/local/calc/vasp/vasp544mpi"]
    run(vasp_command)

    status_code = check_std_log()
    run(["cp", "std.log", "std.log.bak"])

    return status_code


# flake8: noqa: CCR001
def relax_by_vasp(
    incar_relax: str = "INCAR",
    refine_poscar: bool = False,
    run_static: bool = False,
    max_iterations: int = 10,
) -> str:
    """Relax by VASP

    Args:
        incar_relax (str, optional): INCAR for relaxation in current directory.
            Defaults to "INCAR".
        refine_poscar (bool, optional): Whether to refine POSCAR or not.
            Defaults to False.
        run_static (bool, optional): Whether to run extra static calculation or not.
            Defaults to False.
        max_iterations (int, optional): The maximum of iterations. Defaults to 10.

    Returns:
        str: The status code.
    """
    n_core = multiprocessing.cpu_count()
    vasp_command = ["mpirun", "-np", str(n_core), "/usr/local/calc/vasp/vasp544mpi"]

    if run_static:
        if Path("KPOINTS-relax").exists():
            run(["cp", "KPOINTS-relax", "KPOINTS"])
    if incar_relax != "INCAR":
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
    status_code = "SUCCESS"
    for i in range(max_iterations):
        run(vasp_command)

        status_code = check_std_log()
        run(["cp", "std.log", "std.log.bak"])
        if status_code != "SUCCESS":
            break

        if max_iterations == 1:
            break

        vasprun_id = str(vasprun_id_begin + i).zfill(2)
        run(["cp", "CONTCAR", "POSCAR"])
        run(["cp", "CONTCAR", f"CONTCAR_{vasprun_id}"])

        if refine_poscar:
            refine_poscar_file()

        run(["cp", "vasprun.xml", f"vasprun_{vasprun_id}.xml"])

        vasprun = Vasprun(
            "vasprun.xml", parse_dos=False, parse_eigen=False, parse_potcar_file=False
        )
        if (i >= 1) and vasprun.converged_ionic:
            break

    if run_static and (status_code == "SUCCESS"):
        if Path("KPOINTS-final").exists():
            run(["cp", "KPOINTS-final", "KPOINTS"])
        run(["cp", "INCAR-final", "INCAR"])
        run(vasp_command)

    return status_code
