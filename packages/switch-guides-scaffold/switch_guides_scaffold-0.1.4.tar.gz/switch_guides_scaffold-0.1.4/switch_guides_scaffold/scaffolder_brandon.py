import os
import uuid
import click
from click_help_colors import HelpColorsGroup
import logging

# Click groups
@click.group()
def cli():
    """
    Main group responsible for the CLI interace. All commands will be registered to it.
    """
    logging.info(f"Switch CLI started.")
    return None

@click.group()
def guides():
    logging.info(f"Guides.")
    return None

cli.add_command(guides)

if __name__ == "__main__":
    cli()
