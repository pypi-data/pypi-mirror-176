import click
import logging
import switch_guides_scaffold.taskinsights.enums as ti_enums
import switch_guides_scaffold.taskinsights.validation as ti_validation
import switch_guides_scaffold.taskinsights.transformations as ti_transformations
import typing
from io import StringIO
import jinja2
import os
import uuid
import pandas as pd
import switch_api as sw
import collections

# Registering the main group
@click.group()
def taskinsights():
    logging.info(f"Task Insights.")
    return None


@taskinsights.command()
@click.option(
    "--name",
    type=click.types.STRING,
    prompt="Provide a name of the task.",
    help="<Insert docstring for task type selection here.>",
)
@click.option(
    "--task-type",
    type=click.Choice(ti_enums.TASK_TYPES, case_sensitive=False,),
    prompt="Select the type of task to be created. Note that depending on the task selected, the deployment options may vary.",
    help="<Insert docstring for task type selection here.>",
)
@click.option(
    "--description",
    type=click.types.STRING,
    callback=ti_validation.validate_description,
    prompt="Provide a brief description of the task.",
    help="Fills in the description abstractmethod of the task.",
)
@click.option(
    "--readings-type",
    type=click.Choice(ti_enums.MAPPING_ENTITIES, case_sensitive=False,),
    prompt="Select the class of readings that this data ingestion is meant for.",
    help="<Insert docstring for task type selection here.>",
)
@click.option(
    "--author",
    type=click.types.STRING,
    prompt="Provide a brief description of the task.",
    help="Fills in the description abstractmethod of the task.",
)  # Potentially use the local token to fill in this field in the future.
def create_task(
    name: str, task_type: str, description: str, readings_type: str, author: str
):

    # Loading the template into the environment
    template_location: str = str(
        os.path.dirname(os.path.abspath(__file__))
    ) + r"\templates"
    loader = jinja2.loaders.FileSystemLoader(template_location)
    env = jinja2.environment.Environment(loader=loader)
    template = env.get_template("python_drivers.py.jinja2")

    # Preparing the variables for rendering
    generated_uuid: uuid.UUID = uuid.uuid4()

    output = template.render(
        name=name,
        task_type=task_type,
        uuid=generated_uuid,
        readings_type=readings_type,
        description=description,
        author=author,
    )
    print(output)


@taskinsights.command()
@click.option(
    "--name",
    type=click.types.STRING,
    prompt="Provide a name of the task.",
    help="<Insert docstring for task type selection here.>",
)
@click.option(
    "--filepath",
    type=click.types.STRING,
    callback=ti_validation.validate_filepath,
    prompt="Provide the filepath to the sample file that will be used to build this integration.",
    help="Filepath provided will be used to model the integration steps for this integration.",
)
def integrate_csv(name: str, filepath: str) -> None:

    # CONSTANTS
    CHOICES: typing.Dict[str, str] = {
        "1": "Modify existing column.",
        "2": "Add additional column.",
        "3": "Remove an existing column.",
        "4": "Exit the manipulation step.",
        "U": "Undo the previous step.",
    }

    # Setting Pandas display options
    pd.options.display.max_rows = 6
    pd.options.display.max_columns = None  # type: ignore - Displays all columns.
    pd.options.display.max_colwidth = None  # type: ignore - No limit on the column width.
    pd.options.display.expand_frame_repr = (
        False  # Prevents the printed dataframe from wrapping around
    )
    
    # Intializing the actions queue
    # The purpose of the deque is to allow a maximum amount of backtracking
    df_cache: collections.deque[pd.DataFrame] = collections.deque(maxlen=5) # Arbitarily set to 5 for now.
    code_gen: collections.deque[str] = collections.deque()

    # Initializing the api_inputs
    api_project_id: str = "758c3062-dc2f-4550-ae32-00e5b0f46dc8"  # Pointing towards Data Science - EA - Test - Brandon
    click.echo(f"Checking Switch credentials...")
    api_inputs = sw.initialize(
        api_project_id=api_project_id  # type: ignore
    )
    click.echo(f"Switch credentials validated!")

    # Opening the file
    df = pd.read_csv(filepath_or_buffer=filepath)
    print(f"Working Dataframe:")
    click.echo(df)

    # Manipulating the dataframe
    # actions: typing.List[str] = [] 
    while True:
        print(f"Select the following options for transforming your dataframe: ")
        for k, v in CHOICES.items():
            print(f"{k} - {v}")

        selected_choice: str = click.prompt(
            "Enter your selected choice: ",
            type=click.Choice(list(CHOICES.keys()), case_sensitive=False),
        )
        
        if selected_choice == "1": # Selected the option to modify the column
            df = ti_transformations.modify_column(df)
        elif selected_choice == "2":
            df = ti_transformations.add_column(df, code_gen, df_cache)
        elif selected_choice == "U":
            if click.prompt(text=f"Are you sure you want to undo the previous operation?", type=click.Choice(["Y", "N"], case_sensitive=False)) == "Y":
                click.echo(f"Attempting to undo previous step.")
                if len(df_cache) == 0:
                    click.echo(f"Cannot undo anymore.")
                else:
                    df = df_cache.pop() # Restores to the previous version
                    code_gen.pop() # Removes the last element of the code gen
                    click.echo(f"Undo operation successful.")
                    click.echo(df)
        else:
            print(f"No further manipulations can be done to the table.")
            break
        
    # Loading the template into the environment
    template_location: str = str(
        os.path.dirname(os.path.abspath(__file__))
    ) + r"\templates"
    loader = jinja2.loaders.FileSystemLoader(template_location)
    env = jinja2.environment.Environment(loader=loader)
    template = env.get_template(r"integrate_csv.py.jinja2")

    # Preparing the variables for rendering
    generated_uuid: uuid.UUID = uuid.uuid4()

    output = template.render(
        name=name,
        task_type="IntegrationTask",
        uuid=generated_uuid,
        readings_type="Readings",
        description="foo",
        author="bar",
        code_blocks = code_gen
    )
    print(output)


# @taskinsights.command()
# @click.option(
#     "--name",
#     prompt="Enter your name",
#     help="Name for this."
# )
# @click.option(
#     "--number",
#     prompt="Enter your number",
#     help="Number for this."
# )
# def test(name, number):
#     print(name)
#     print(number)
