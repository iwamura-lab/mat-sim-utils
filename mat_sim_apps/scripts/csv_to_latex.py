from typing import List

import click


def create_latex_table(csv_lines: List[str]) -> str:
    """Create LaTeX table code from lines of a CSV file

    Args:
        csv_lines (List[str]): The lines of a CSV file.

    Returns:
        str: The LaTeX table code.
    """
    n_column = csv_lines[0].count(",") + 1

    # Create the lines of a LaTeX table code
    lines = [f"\\begin{{tabular}}{{{' '.join('l' * n_column)}}} \\\\ \\hline \\hline"]
    lines.append(f"{' & '.join(csv_lines[0].split(','))} \\\\ \\hline")
    for csv_line in csv_lines[1:]:
        lines.append(f"{' & '.join(csv_line.split(','))} \\\\")
    lines[-1] += " \\hline \\hline"
    lines.append("\\end{tabular}")

    content = "\n".join(lines)

    return content


@click.command()
@click.argument("csv_file")
def main(csv_file) -> None:
    """Create LaTeX table code from a CSV file"""
    with open(csv_file) as f:
        lines = [line.strip() for line in f]

    # Create a LaTeX code
    content = create_latex_table(lines)
    print(content)
