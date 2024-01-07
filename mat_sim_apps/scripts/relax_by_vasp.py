import click

from mat_sim_apps.bin import relax_by_vasp


@click.command()
@click.option("--run_static/--no-run_static", default=False, show_default=True)
def main(run_static) -> None:
    relax_by_vasp(run_static=run_static)
