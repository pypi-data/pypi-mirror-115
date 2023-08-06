import click
import json

from ranger_cli.utils import CONTEXT_SETTINGS, response_and_exit
from ranger_cli.config import provide_ranger_client
from ranger_cli.client import RangerClient
from ranger_cli.cli_options import (
    config_option,
    profile_option,
    service_name_option,
    service_id_option
)


@click.group(context_settings=CONTEXT_SETTINGS)
@profile_option()
def service():
    """
    Administration for Apache Ranger's service public REST API.
    """
    pass


@service.command(context_settings=CONTEXT_SETTINGS)
@service_id_option(mutually_exclusive=["service_name"])
@service_name_option(mutually_exclusive=["service_id"])
@provide_ranger_client
@response_and_exit
def get(ranger_client: RangerClient, service_id: int, service_name: str):
    """
    Searches for Apache Ranger service repository (or repositories).
    """
    if service_id:
        return ranger_client.get_service_by_id(service_id)
    if service_name:
        return ranger_client.get_service_by_name(service_name)

    return ranger_client.get_services()


@service.command(context_settings=CONTEXT_SETTINGS)
@config_option(required=True)
@provide_ranger_client
@response_and_exit
def create(ranger_client: RangerClient, config: str):
    """
    Creates a new Apache Ranger service repository.
    """
    return ranger_client.create_service(json.loads(config))


@service.command(context_settings=CONTEXT_SETTINGS)
@service_id_option(required=True)
@config_option(required=True)
@provide_ranger_client
@response_and_exit
def update(ranger_client: RangerClient, service_id: int, config: str):
    """
    Updates an existing Apache Ranger service repository.
    """
    return ranger_client.update_service(service_id, json.loads(config))


@service.command(context_settings=CONTEXT_SETTINGS)
@service_id_option(required=True)
@provide_ranger_client
@response_and_exit
def delete(ranger_client: RangerClient, service_id: int):
    """
    Deletes an existing Apache Ranger service repository.
    """
    return ranger_client.delete_service(service_id)
