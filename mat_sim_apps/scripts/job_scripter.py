import logging
from pathlib import Path

import click

from mat_sim_apps.fileio import create_job_script


@click.command()
@click.argument("command", nargs=-1)
@click.option("-j", "--job_name", help="The name of a job.")
def main(command, job_name) -> None:
    """Create a job script which execute a given command"""
    logging.basicConfig(level=logging.INFO)

    logging.info(" Configuration")
    logging.info(f"   command  : {' '.join(command)}")
    logging.info(f"   job name : {job_name}")

    logging.info(" Make calculation directory, 'work'")

    pool_dir_path = Path.cwd() / "work"
    if not pool_dir_path.exists():
        pool_dir_path.mkdir()

    output_dir_path = pool_dir_path / job_name
    output_dir_path.mkdir()

    logging.info(" Write a job script")

    content = create_job_script(command, job_name)
    job_script_path = output_dir_path / "job.sh"
    with job_script_path.open("w") as f:
        f.write(content)
