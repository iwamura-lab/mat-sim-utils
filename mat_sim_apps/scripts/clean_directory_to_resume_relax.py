from pathlib import Path
from subprocess import run
from typing import List

import click

UNUSED_FILE_LIST = [
    "CHG",
    "CHGCAR",
    "CONTCAR",
    "DOSCAR",
    "EIGENVAL",
    "err.log",
    "IBZKPT",
    "OSZICAR",
    "OUTCAR",
    "PCDAT",
    "REPORT",
    "vasprun.xml",
    "WAVECAR",
    "XDATCAR",
]


def find_end_line_number(std_lines: List[str]) -> int:
    """Find the end line number in std.log

    Args:
        std_lines (List[str]): The lines of std.log.

    Returns:
        int: The end line number.
    """
    line_number = len(std_lines) - 1
    while "running on " not in std_lines[line_number]:
        line_number -= 1

    return line_number


def count_vasp_execution(std_lines: List[str]) -> int:
    """Count VASP execution

    Args:
        std_lines (List[int]): The lines of std.log.

    Returns:
        int: How many times VASP was executed.
    """
    cnt = 0
    for line in std_lines:
        if "running on " in line:
            cnt += 1

    return cnt


@click.command
def main() -> None:
    """Clean directory to resume paused relaxation"""
    # Delete lines in std.log about paused relaxation
    with open("std.log") as f:
        lines = f.readlines()
    end_line_number = find_end_line_number(lines)

    with open("std.log", "w") as f:
        f.write("".join(lines[:end_line_number]))

    # Delete unused files
    for file in UNUSED_FILE_LIST:
        Path(file).unlink()

    # Delete kept files
    with open("std.log") as f:
        lines = f.readlines()
    n_vasp_execution = count_vasp_execution(lines)
    vasp_execution_id = str(n_vasp_execution + 1).zfill(2)

    Path(f"CONTCAR_{vasp_execution_id}").unlink()
    Path(f"vasprun_{vasp_execution_id}.xml").unlink()

    # Copy CONTCAR as POSCAR
    run(["cp", f"CONTCAR_{str(n_vasp_execution).zfill(2)}", "POSCAR"])
