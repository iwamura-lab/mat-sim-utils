import logging
import os
import shutil
from pathlib import Path
from subprocess import run

import click

from mat_sim_apps.fileio import create_job_script


@click.command()
@click.argument("commands")
@click.option("-j", "--job_name", help="The name of a job.")
def main(commands, job_name) -> None:
    """Create a job script which execute given commands

    \b
    It is possible to execute multiple commands.
    Example)
    job_scripter "ls ~:cat ~/.zshrc"
    """
    logging.basicConfig(level=logging.INFO)

    logging.info(" Configuration")
    logging.info(f"   command  : {' '.join(commands)}")
    logging.info(f"   job name : {job_name}")

    logging.info(" Make calculation directory, 'work'")

    cwd_dir_path = Path.cwd()
    output_dir_path = cwd_dir_path / "work" / job_name
    if output_dir_path.exists():
        shutil.rmtree(output_dir_path)

    output_dir_path.mkdir(parents=True)

    logging.info(" Write a job script")

    command_list = commands.split(":")
    content = create_job_script(command_list, job_name, venv_name="csp_scipy")

    job_script_path = output_dir_path / "job.sh"
    with job_script_path.open("w") as f:
        f.write(content)

    # Submit a job
    os.chdir(output_dir_path)
    run(["sbatch", "job.sh"])
    os.chdir(cwd_dir_path)
