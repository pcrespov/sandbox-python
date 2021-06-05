import logging
import sys
import os
from pathlib import Path
from pprint import pformat
from typing import Optional

import click
from pydantic.env_settings import BaseSettings
import yaml
#from app_settings_1 import Settings2, create_factory, create_settings_class
from app_settings import Settings

from pydantic import ValidationError

log = logging.getLogger()


def print_envs(settings_obj):
    for name in settings_obj.__fields__:
        value = getattr(settings_obj, name)
        if isinstance(value, BaseSettings):
            click.echo(f"\n# {name}")
            print_envs(value)
        else:
            field_info = settings_obj.__fields__[name].field_info
            if field_info.description:
                click.echo(f"# {field_info.description}" )
            click.echo(f"{name}={value}")

def print_as_json(settings_obj):
    click.echo(settings_obj.json(indent=2))



# TODO: typer
@click.command("Some 12-factor app CLI")
@click.option(
    "--print-settings-env",
    "-C",
    default=False,
    is_flag=True,
    help="Resolves settings, prints env vars and exits",
)
@click.option(
    "--print-settings-json",
    default=False,
    is_flag=True,
    help="Resolves settings, prints as json and exits",
)
@click.option(
    "--print-settings-json-schema",
    default=False,
    is_flag=True,
    help="Prints settings json-schema and exits",
)
def main(print_settings_env: bool = False, print_settings_json: bool = False, print_settings_json_schema: bool = False):

    if print_settings_json_schema:
        click.echo(Settings.schema_json(indent=2))
        sys.exit(os.EX_OK)


    try:
        # from app_settings import create_factory
        #settings_factory = create_factory()
        #settings: settings_factory.Settings = settings_factory.create(**config_values)
        settings = Settings.create_from_env()

    except ValidationError as err:
        # TODO: validation error

        HEADER = "{:-^50}"
        log.error(
            "Invalid settings. %s:",
            err,
            # HEADER.format("schema"),
            # Settings.schema_json(indent=2),
            # HEADER.format("environment variables"),
            # pformat(dict(os.environ)),
            exc_info=False,
        )
        sys.exit(os.EX_DATAERR)

    if print_settings_json:
        print_as_json(settings)

    if print_settings_env:
        print_envs(settings)

    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()

#  print(Settings())
#  print(Settings(settings2={"some_other_value": 55}))
#  print(Settings2.create_from_environ(settings1={"value":33}))
