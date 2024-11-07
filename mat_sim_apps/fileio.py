from typing import List


def create_job_script(command_list: List[str], job_name: str, venv_name: str) -> str:
    """Create job script

    Args:
        command_list (List[str]): List of executed commands.
        job_name (str): The name of a job.
        venv_name (str): The name of a Python virtual environment.

    Returns:
        str: The content of a job script.
    """
    lines = [
        "#!/bin/zsh",
        f"#SBATCH -J {job_name}",
        "#SBATCH --nodes=1",
        "#SBATCH -o std.log",
        "#SBATCH -e err.log",
        "#SBATCH --open-mode=append",
        "",
        "export MPI_PATH=/usr/local/calc/openmpi-gcc",
        "export PATH=${MPI_PATH}/bin:${PATH}",
        "export LD_LIBRARY_PATH=${MPI_PATH}/lib:${LD_LIBRARY_PATH}",
        "",
        ". ~/.zprofile",
        ". ~/.zshrc",
        f"pyenv activate {venv_name}",
    ]
    lines.extend(command_list)
    lines.append("")
    content = "\n".join(lines)

    return content
