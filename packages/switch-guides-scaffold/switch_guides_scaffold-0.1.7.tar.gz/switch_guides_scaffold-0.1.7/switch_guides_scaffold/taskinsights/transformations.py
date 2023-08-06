import pandas as pd
import switch_api as sw
import click
import typing
import collections
import re
import datetime

# def lambda_builder(input: str) -> typing.Callable[..., typing.Any]:

#     """
#     The purpose of this function is to take a lambda function written as a string and parse it into a proper lambda function
#     """


def modify_column(df) -> pd.DataFrame:

    # Getting the list of columns currently present within the dataframe
    existing_columns: typing.Set[str] = set(df.columns)

    # selected_column = ""
    # while selected_column not in existing_columns:
    #     if selected_column != "":
    #         click.echo(f"Selected column {selected_column} does not exist within the list of column headers.")
    #     selected_column: str = click.prompt("Please enter a column name that needs to be modified.", type=click.types.STRING)

    click.echo(
        f"Enter a lambda function using the form lambda syntax. \n For instance 'lambda [col A], [col B]: [col A] + [col B]'. "
    )
    return df


def add_column(df: pd.DataFrame, code_gen: collections.deque[str], df_cache: collections.deque[pd.DataFrame]):

    COLUMN_VALUE_OPTION: typing.Dict[str, str] = {
        "1": "Copy from existing column.",
        "2": "Insert a common value across all records.",
        "3": "Generate values from existing columns.",
    }

    # Getting the user intput for the column name
    column_name: str = click.prompt(
        text=f"Provide the name of the new column.", type=click.types.STRING
    )
    
    if column_name in set(df.columns):
        click.echo(f"Column name already exists, and thus the existing column will be overwritten. Continue?")
        if click.prompt("Y/N") =="N":
            return df
    
    # Making a copy of the original dataframe
    df_original: pd.DataFrame = pd.DataFrame(
        data=df,
        copy=True
    )

    # Getting the user input for the value that needs to be generated
    print(f"Select the following options for generating the new column: ")
    for k, v in COLUMN_VALUE_OPTION.items():
        print(f"{k} - {v}")

    selected_choice: str = click.prompt(
        "Enter your selected choice: ",
        type=click.Choice(list(COLUMN_VALUE_OPTION.keys()), case_sensitive=False),
    )

    if selected_choice == "1":
        existing_column_name: str = click.prompt(
            f"Select a existing column",
            type=click.Choice(list(df.columns), case_sensitive=False),
        )
        try:
            df[column_name] = df[existing_column_name]
            click.echo(f"Created the column {column_name}!")
            click.echo(df)
        except Exception as e:
            click.echo(f"Unable to perform this operation. See error message raised: {e}")
            return df
        
        # Updating the code gen and the cache
        df_cache.append(df_original)
        code_gen.append(f'df["{column_name}"] = df["{existing_column_name}"]')
    
    if selected_choice == "2":
        
        input_value_raw: str = click.prompt(
            text=f"Provide the value used to populate this column: ",
            type=click.types.STRING
        )
        
        is_numeric: bool = False
        if str.isnumeric(input_value_raw):
            click.echo(f"The input appears to be a numeric value. Evaluate it as a numeric value?")
            if click.prompt(text="Y/N") == "Y":
                is_numeric = True
        
        try:
            if is_numeric:
                df[column_name] = float(input_value_raw)
                code_gen.append(f'df["{column_name}"] = float({input_value_raw})')
            else:
                df[column_name] = str(input_value_raw)
                code_gen.append(f'df["{column_name}"] = str({input_value_raw})')
            click.echo(f"Created the column {column_name} and set the value == {input_value_raw}")
            click.echo(df)
        except Exception as e:
            click.echo(f"Unable to perform this operation. See error message raised: {e}")
            return df
        
        df_cache.append(df_original)
    
    if selected_choice == "3":
        # Concept: Allows python expressions to be written, but the variable names are substituted with column names instead.
        # E.g. ["Column A"].contains("foo") -> outputs a boolean column
        
        COLUMN_REGEX_PATTERN: str = r'(\["[A-z0-9 ]+"\])'
        
        input_function_raw: str = click.prompt(
            text=f"Provide the function that will be applied elementwise: ",
            type=click.types.STRING
        )
        
        # Validating that the input column names are valid (Present within the actual dataframe)
        c: str
        for c in re.findall(COLUMN_REGEX_PATTERN, input_function_raw):
            if c[2:-2] not in df.columns:
                click.echo(f"Column \"{c[2:-2]}\" appears to not be present.")
                return df
        
        # Converting into a lambda function
        lambda_function_str: str = re.sub(
            pattern=COLUMN_REGEX_PATTERN,
            repl=r"row\1",
            string=input_function_raw
        )
        
        # Executing the actual function
        try:
            exec(f'df["{column_name}"] = df.apply(lambda row: {lambda_function_str}, axis = 1)')
            click.echo(df)
            code_gen.append(f'df["{column_name}"] = df.apply(lambda row: {lambda_function_str}, axis = 1)')
        except Exception as e:
            click.echo(f"Unable to perform this operation. See error message raised: {e}")
            return df
        
        # Storing the original into the cache
        df_cache.append(df_original)
        
        return df
        
    return df
        
