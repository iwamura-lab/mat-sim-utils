import glob
import re
from itertools import chain

import click


@click.command()
@click.argument("new_version_num", nargs=1)
def cli(new_version_num):
    """This script changes package's version number."""
    setup_files = chain(
        glob.glob("**/setup.py", recursive=True),
        glob.glob("**/setup.cfg", recursive=True),
    )
    for setup_file in setup_files:
        with open(setup_file, "r") as f:
            lines = f.readlines()
        with open(setup_file, "w") as f:
            new_lines = [
                re.sub(r"[0-9]+.[0-9]+.[0-9]+", new_version_num, line)
                if "version" in line
                else line
                for line in lines
            ]
            for line in new_lines:
                f.write(line)
