import subprocess
import time

import click


@click.command()
@click.option(
    "--user_name", default="iwamura", show_default=True, help="Your user name."
)
def main(user_name) -> None:
    """Show current memory allocation on each node"""
    show_job_name_command = " ".join(
        [f"squeue | grep {user_name} |", "grep ' R ' | awk '{print $1,$3}'"]
    )
    result = subprocess.run(show_job_name_command, shell=True, stdout=subprocess.PIPE)
    stdout = result.stdout.decode("utf-8")
    time.sleep(0.1)

    # Make jid_to_job_name dict
    jid_to_job_name = {
        line.split()[0]: line.split()[1] for line in stdout.split("\n")[:-1]
    }

    show_mem_alloc_command = (
        f"for jid in $(squeue | grep {user_name} | grep ' R '"
        "| awk '{print $1}'); do sstat -n -j ${jid} -o JobID,MaxRSS; done"
    )
    result = subprocess.run(show_mem_alloc_command, shell=True, stdout=subprocess.PIPE)
    stdout = result.stdout.decode("utf-8")

    # Process stdout
    jid_mem_alloc_list = [
        [item for item in line.split()] for line in stdout.split("\n")[:-1]
    ]
    jids, mem_allocs = zip(*jid_mem_alloc_list)
    mem_allocs_gb = []
    for mem_alloc in mem_allocs:
        unit_conversion_factor = 2
        if "M" in mem_alloc:
            unit_conversion_factor = 1
        mem_allocs_gb.append(float(mem_alloc[:-1]) / (1024**unit_conversion_factor))

    # Pretty-print stdout
    print("    NAME mem_alloc (GB)")
    for jid, mem_alloc in zip(jids, mem_allocs_gb):
        job_name = jid_to_job_name[jid.split(".")[0]]
        output_line = " ".join([job_name.rjust(8), f"{mem_alloc:.1f}"])
        print(output_line)
