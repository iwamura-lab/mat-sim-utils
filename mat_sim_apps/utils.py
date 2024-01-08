import re


def extract_vasprun_id(filename: str) -> int:
    """Extract vasprun_id from the filename of vasprun.xml

    Args:
        filename (str): The filename of a vasprun.xml.

    Returns:
        int: vasprun_id.
    """
    vasprun_xml_pattern = re.compile(r"vasprun_(\d+)\.xml")
    m = vasprun_xml_pattern.match(filename)
    assert m is not None
    return int(m.group(1))
