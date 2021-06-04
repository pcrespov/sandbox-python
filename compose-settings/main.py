import logging
import sys
import os
from pathlib import Path
from pprint import pformat
from typing import Optional

import click
import yaml
from app_settings import Settings2, create_factory, create_settings_class

from pydantic import ValidationError

log = logging.getLogger()



# TODO: typer
@click.command("")
@click.option(
    "--settings-path",
    default=None,
    type=click.Path(exists=False, path_type=str),
)
@click.option(
    "--check-settings",
    "-C",
    default=False,
    is_flag=True,
    help="Checks settings, prints and exits",
)
@click.option(
    "--settings-json-schema",
    default=False,
    is_flag=True,
    help="Prints settings json-schema and exits",
)
def main(settings_path: Optional[Path] = None, check_settings: bool = False, settings_json_schema: bool = False):

    config_values = {}

    if settings_path:
        config_values = yaml.loads(settings_path.read_text())

    Settings = create_settings_class()

    if settings_json_schema:
        click.echo(Settings.schema_json(indent=2))
        sys.exit(os.EX_OK)


    try:
        # from app_settings import create_factory
        #settings_factory = create_factory()
        #settings: settings_factory.Settings = settings_factory.create(**config_values)

        settings = Settings(**config_values)

    except ValidationError as err:
        # TODO: validation error

        HEADER = "{:-^50}"
        log.error(
            "Invalid settings. %s:" + "\n%s"*6,
            err,
            HEADER.format("schema"),
            Settings.schema_json(indent=2),
            HEADER.format("config_dict"),
            pformat(config_values),
            HEADER.format("environment variables"),
            pformat(dict(os.environ)),
            exc_info=False,
        )
        sys.exit(os.EX_DATAERR)

    if check_settings:
        click.echo(settings.json(indent=2))
        sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()

#  print(Settings())
#  print(Settings(settings2={"some_other_value": 55}))
#  print(Settings2.create_from_environ(settings1={"value":33}))
