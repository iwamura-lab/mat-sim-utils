import os
from pathlib import Path
from subprocess import run

import click

from mat_sim_apps.fileio import create_job_script


@click.command()
@click.argument("n_job", type=int)
@click.option(
    "-p",
    "--partition",
    default="vega-a,vega-c,vega-d",
    show_default=True,
    help="The name of partition.",
)
def main(n_job, partition) -> None:
    """Keep n_job resources on VEGA"""
    # Set an command which sleeps for a day
    command = ["sleep", "1d"]

    root_dir_path = Path.cwd().resolve() / "resource_keeper"
    root_dir_path.mkdir()

    for i in range(n_job):
        # Make calculation directory
        job_id = str(i + 1).zfill(2)
        output_dir_path = root_dir_path / job_id
        output_dir_path.mkdir()

        # Write a job script
        content = create_job_script(command, job_name=f"test-{job_id}")
        job_script_path = output_dir_path / "job.sh"
        with job_script_path.open("w") as f:
            f.write(content)

        # Submit a job
        os.chdir(output_dir_path)
        run(["sbatch", "-p", partition, "job.sh"])
