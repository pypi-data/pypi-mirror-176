import click
import logging
import switch_guides_scaffold.taskinsights.enums as switch_enums
import typing
import os


def validate_description(ctx: click.Context, param: click.Parameter, value: typing.Any):
    while len(value) > 100:
        click.echo(
            "Description is too verbose. Please re-enter a concise description: "
        )
        value = click.prompt("", type=click.types.STRING,)
    return value


def validate_filepath(ctx: click.Context, param: click.Parameter, value: str) -> str:

    # Defining an error_flag
    error_flag: bool = False
    value = str(value)

    # Checking if the filepath is valid
    error_flag = len(value) == 0
    while error_flag:
        click.echo("No filepath is provided. Please enter a proper filepath.")
        value = click.prompt("", type=click.types.STRING,)
        error_flag = len(value) == 0

    # Checking if the filepath exists
    error_flag = os.path.exists(value)
    while not error_flag:
        click.echo("File path does not exist. Please enter a valid filepath.")
        value = click.prompt("", type=click.types.STRING,)
        error_flag = os.path.exists(value)

    # Checking if the filepath exists
    error_flag = os.path.isfile(value)
    while not error_flag:
        click.echo("No file at the provided filepath. Please enter a valid filepath.")
        value = click.prompt("", type=click.types.STRING,)
        error_flag = os.path.isfile(value)

    # Checking if the file is a csv type.
    # NOTE: This is a relatively trivial check that can be easily overcome - Needs improvement as development progresses.
    error_flag = value[-4:] == ".csv"
    while not error_flag:
        click.echo("The provided file does not appear to be of a csv type.")
        value = click.prompt("", type=click.types.STRING,)
        error_flag = value[-4:] == ".csv"

    return str(value)
