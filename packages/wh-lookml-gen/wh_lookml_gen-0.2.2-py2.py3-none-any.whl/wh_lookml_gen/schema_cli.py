"""Console script for wh_lookml_gen."""
import sys
import click

from .dbt_test_gen import schema_output

@click.command()
def schema(args=None):
    """Console script for wh_lookml_gen."""
    click.echo("Replace this message by putting your code into "
               "wh_lookml_gen.cli.schema_output")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return schema_output()

