import os
import subprocess
import time
from pathlib import Path

import click


def make_job_script(name: str, core: int) -> str:
    job_script_content = (
        "#######################################################################\n"
        "#$ -S /bin/zsh\n"
        "#$ -cwd\n"
        f"#$ -N {name}\n"
        "#$ -o std.log\n"
        "#$ -e err.log\n"
        f"#$ -pe mpi* {core}\n"
        "#######################################################################\n"
        "# save initial structure\n"
        "cp -rf POSCAR POSCAR.init\n"
        "\n"
        "/usr/local/calc/openmpi-gcc/bin/mpirun /usr/local/calc/vasp/vasp544mpi\n"
    )

    return job_script_content


@click.command()
@click.option(
    "--min_id", required=True, type=int, help="minimum id of searching directories"
)
@click.option(
    "--max_id", required=True, type=int, help="maximum id of searching directories"
)
@click.option("-q", "--que", default="vega-a", show_default=True, help="group name")
@click.option(
    "--prefix",
    default="disp-",
    show_default=True,
    help="prefix of the searching directories",
)
@click.option(
    "--id_digits", type=int, default=3, show_default=True, help="digits filled by zero"
)
def main(min_id, max_id, que, prefix, id_digits):
    """Usefull package to submit multiple VASP jobs"""
    root_dir_path = Path.cwd()
    inputs_dir_path_list = [
        root_dir_path / "".join([prefix, str(dir_id).zfill(id_digits)])
        for dir_id in range(min_id, max_id + 1)
    ]

    for dir_path in inputs_dir_path_list:
        if not dir_path.exists():
            continue

        if que == "vega-c":
            core = 32
        else:
            core = 16

        job_script_path = dir_path / "job.sh"
        with job_script_path.open("w") as f:
            name = dir_path.stem
            job_script_content = make_job_script(name, core)
            f.write(job_script_content)

        os.chdir(dir_path)
        subprocess.call(f"qsub -q {que} job.sh", shell=True)
        os.chdir(root_dir_path)

        # wait for safety
        time.sleep(0.1)
