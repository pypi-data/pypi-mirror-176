import click
import logging

@click.group()
def guides():
    logging.info(f"Guides.")
    return None

