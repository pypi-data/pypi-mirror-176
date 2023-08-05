from pathlib import Path
from datetime import datetime

import click

from .scripts import Generate
from .errors import FileError, InternalError

cli: click.Group
now = datetime.now()
formated_now = now.strftime("%Y-%m-%d %H:%M:%S")


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.option("-i", "--input", required=True, type=Path)
@click.option("-t", "--template", required=True, type=Path)
@click.option(
    "-f",
    "--input-format",
    default="xlsx",
    type=click.Choice(["xlsx"], case_sensitive=False),
)
@click.option(
    "-o",
    "--output",
    default=Path(f"./autodocx-{formated_now}"),
    type=Path,
)
@click.option(
    "-d",
    "--document-name-column",
    default="Document Name",
    type=str,
)
def basic(
    input: Path,
    input_format: str,
    template: Path,
    output: Path,
    document_name_column: str,
):
    # Validation
    if not input.exists():
        raise click.exceptions.FileError("Input file doesn't exists.")

    if not template.exists():
        raise click.exceptions.FileError("Input file doesn't exists.")

    click.echo("Generating docs...")

    try:
        Generate(
            input=input,
            input_format=input_format,
            template=template,
            output=output,
            document_name_column=document_name_column,
        ).run()
    except FileError as e:
        raise click.FileError(e)
    except InternalError as e:
        raise click.exceptions.Exit(e)
