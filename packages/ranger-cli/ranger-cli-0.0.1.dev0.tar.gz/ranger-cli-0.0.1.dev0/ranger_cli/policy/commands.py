import click
import json

from ranger_cli.utils import CONTEXT_SETTINGS, response_and_exit
from ranger_cli.cli_types import MutuallyExclusiveOption
from ranger_cli.config import provide_ranger_client
from ranger_cli.client import RangerClient
from ranger_cli.cli_options import (
    policy_id_option,
    policy_name_option,
    service_name_option,
    config_option,
    profile_option
)


@click.group(context_settings=CONTEXT_SETTINGS)
@profile_option()
def policy():
    """
    Administration for Apache Ranger's policy public REST API.
    """
    pass


@policy.command(context_settings=CONTEXT_SETTINGS)
@policy_id_option(mutually_exclusive=["policy_name", "service_name"])
@policy_name_option(mutually_exclusive=["policy_id", "service_name"])
@service_name_option(mutually_exclusive=["policy_id", "policy_name"])
@provide_ranger_client
@response_and_exit
def get(ranger_client: RangerClient, policy_id: int, policy_name: str, service_name: str):
    """
    Searches for Apache Ranger resource-based policy (or policies).
    """
    if policy_id:
        return ranger_client.get_policy_by_id(policy_id)
    if policy_name:
        return ranger_client.get_policy_by_name(policy_name)
    if service_name:
        return ranger_client.get_service_policies(service_name)

    return ranger_client.get_policies()


@policy.command(context_settings=CONTEXT_SETTINGS)
@config_option(required=True)
@provide_ranger_client
@response_and_exit
def create(ranger_client: RangerClient, config: str):
    """
    Creates a new Apache Ranger resource-based policy.
    """
    return ranger_client.create_policy(json.loads(config))


@policy.command(context_settings=CONTEXT_SETTINGS)
@policy_id_option(required=True)
@config_option(required=True)
@provide_ranger_client
@response_and_exit
def update(ranger_client: RangerClient, policy_id: int, config: str):
    """
    Updates an existing Apache Ranger resource-based policy.
    """
    return ranger_client.update_policy(policy_id, json.loads(config))


@policy.command(context_settings=CONTEXT_SETTINGS)
@policy_id_option(required=True)
@provide_ranger_client
@response_and_exit
def delete(ranger_client: RangerClient, policy_id: int):
    """
    Deletes an existing Apache Ranger resource-based policy.
    """
    return ranger_client.delete_policy(policy_id)
