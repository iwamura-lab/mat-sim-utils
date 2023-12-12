from typing import List


def create_job_script(command: List[str], job_name: str) -> str:
    """Create job script

    Args:
        command (List[str]): An executed command.
        job_name (str): The name of a job.

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
        ". ~/.zprofile",
        ". ~/.zshrc",
        "pyenv activate structural_search",
        " ".join(command),
        "",
    ]
    content = "\n".join(lines)

    return content
