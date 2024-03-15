import re
from typing import List

import click


def format_latex_table_item(item: str, column_type: str) -> str:
    """Format an item in LaTeX table

    Args:
        item (str): An item in a LaTeX table.
        column_type (str): The type of the column including the item.

    Returns:
        str: A formatted item.
    """
    if column_type == "formula":
        m = re.match(r"([A-Z][a-z]*)([\d\.]*)([A-Z][a-z]*)([\d\.]*)", item)
        assert m is not None

        elements = []
        comps = []

        if m.group(1) != "":
            elements.append(m.group(1))
        comps.append(m.group(2))
        if m.group(3) != "":
            elements.append(m.group(3))
        comps.append(m.group(4))

        item = "".join(
            f"\\mathrm{{{e}}}" if c == "" else f"\\mathrm{{{e}}}_{{{c}}}"
            for e, c in zip(elements, comps)
        )
        item = f"${item}$"
    elif column_type == "equation":
        m = re.match(r".*(-[a-z\d]).*", item)
        if m is not None:
            s = m.group(1)
            item = item.replace(s, f"\\bar{{{s[-1]}}}")
        item = f"${item}$"

    return item


def create_latex_table(csv_lines: List[str], table_format: str = "") -> str:
    """Create LaTeX table code from lines of a CSV file

    Args:
        csv_lines (List[str]): The lines of a CSV file.
        table_format (str, optional): The comma separated format of each column.
            Defaults to "".

    Returns:
        str: The LaTeX table code.
    """
    n_column = csv_lines[0].count(",") + 1

    # Create the lines of a LaTeX table code
    lines = [f"\\begin{{tabular}}{{{' '.join('l' * n_column)}}} \\\\ \\hline \\hline"]
    lines.append(f"{' & '.join(csv_lines[0].split(','))} \\\\ \\hline")
    for csv_line in csv_lines[1:]:
        items = csv_line.split(",")
        if table_format != "":
            items = [
                format_latex_table_item(item, f)
                for item, f in zip(items, table_format.split(","))
            ]
        lines.append(f"{' & '.join(items)} \\\\")
    lines[-1] += " \\hline \\hline"
    lines.append("\\end{tabular}")

    content = "\n".join(lines)

    return content


@click.command()
@click.argument("csv_file")
@click.option(
    "--table_format",
    default="",
    show_default=True,
    help="The comma separated format of each column.",
)
def main(csv_file, table_format) -> None:
    """Create LaTeX table code from a CSV file"""
    with open(csv_file) as f:
        lines = [line.strip() for line in f]

    # Create a LaTeX code
    content = create_latex_table(lines, table_format)
    print(content)
