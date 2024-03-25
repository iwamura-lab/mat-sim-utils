import pytest

from mat_sim_apps.scripts.csv_to_latex import format_latex_table_item


@pytest.mark.parametrize(
    ("item", "table_format", "expected"),
    [
        ("AlPt", "formula", "$\\mathrm{Al}\\mathrm{Pt}$"),
        ("Al3.92Pt0.08", "formula", "$\\mathrm{Al}_{3.92}\\mathrm{Pt}_{0.08}$"),
        ("Fm-3m", "equation", "$Fm\\bar{3}m$"),
    ],
)
def test_format_latex_table_item(item, table_format, expected):
    assert format_latex_table_item(item, table_format) == expected
