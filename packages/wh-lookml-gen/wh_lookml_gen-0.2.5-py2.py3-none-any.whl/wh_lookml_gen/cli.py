"""Console script for wh_lookml_gen."""
import sys
import click

from .wh_lookml_gen import output


@click.command()
def lookml(args=None):
    """Console script for wh_lookml_gen."""
    click.echo("Replace this message by putting your code into "
              "wh_lookml_gen.cli.lookml")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return output()