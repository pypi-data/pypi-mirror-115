import os
import click
import six
import json
import confuse
import pathlib

from rich.console import Console
from rich.table import Table


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
CONFIG_APP = "ranger"

PROPERTY_LIST = [
    "name",
    "parent",
    "mandatory",
    "recursiveSupported",
    "excludesSupported",
    "matcher",
    "matcherOptions",
    "description",
    "defaultValue",
    "impliedGrants"
]

def get_default_profile():
    configuration = confuse.Configuration("ranger")
    configuration_file = pathlib.Path(configuration.user_config_path())
    if configuration_file.exists():
        try:
            configuration = configuration["default"].get()
        except confuse.exceptions.NotFoundError:
            return next(iter(configuration.get()))
        return "default"
    return None


def read_config(profile: str):
    try:
        configs = confuse.Configuration("ranger")[profile].get()
        return {k: tuple(v) if isinstance(v, list) else v for k, v in configs.items()}
    except confuse.exceptions.NotFoundError as e:
        return None


def exception_response(exception, response) -> str:
    return pretty_response(
        {
            "error_type": exception.__class__.__name__,
            "error": response.status_code,
            "error_summary": response.reason,
            "endpoint": response.url,
        }
    )


def status_response(response) -> str:
    return pretty_response(
        {"status": response.status_code, "status_summary": response.reason}
    )


def pretty_response(response: dict) -> str:
    return json.dumps(response, indent=2)


def response_and_exit(func: callable):
    @six.wraps(func)
    def inner_wrapper(*args: list, **kwargs: dict):
        try:
            response = func(*args, **kwargs)
        except Exception as error:
            click.echo(f"ERROR: {error}")
            exit(1)
        else:
            if response:
                if not isinstance(response, bool):
                    click.echo(response)
            exit(0)

    return inner_wrapper


def table_response_and_exit(property_type: str):
    def inner_function(func):
        @six.wraps(func)
        def inner_wrapper(*args: list, **kwargs: dict):
            service = kwargs["service_type"]
            try:
                response = func(*args, **kwargs)
            except Exception as error:
                click.secho(f"ERROR: {error}", fg="red")
                exit(1)

            table = Table(
                "PROPERTY", "VALUE",
                title=f"{service.upper()} Plugin {property_type.capitalize()}",
                title_style="bold"
            )

            for rows in json.loads(response):
                for properties in rows[property_type]:
                    for key, value in properties.items():
                        if key in PROPERTY_LIST:
                            table.add_row(key, str(value))
                    table.add_row(end_section=True)
            Console().print(table)

        return inner_wrapper
    return inner_function
