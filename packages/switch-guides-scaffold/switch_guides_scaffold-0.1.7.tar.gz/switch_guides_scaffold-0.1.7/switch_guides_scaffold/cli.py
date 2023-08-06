import click
import logging
import switch_api as sw

from switch_guides_scaffold.guides import guides_commands
from switch_guides_scaffold.taskinsights import task_insights

# Click groups
@click.group()
def cli():
    """
    Main group responsible for the CLI interace. All commands will be registered to it.
    """
    logging.info(f"Switch CLI started.")
    return None

cli.add_command(guides_commands.guides)
cli.add_command(task_insights.taskinsights)

if __name__ == "__main__":
    cli()
    
sw.initialize