import click
import json

from ranger_cli.utils import CONTEXT_SETTINGS, response_and_exit, table_response_and_exit
from ranger_cli.config import provide_ranger_client
from ranger_cli.client import RangerClient
from ranger_cli.cli_options import profile_option, service_type_option


@click.group(context_settings=CONTEXT_SETTINGS)
@profile_option()
def servicedef():
    """
    Administration for Apache Ranger's servicedef public REST API.
    """
    pass


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@provide_ranger_client
@service_type_option()
@response_and_exit
def get(ranger_client: RangerClient, service_type: str):
    """
    Searches for Apache Ranger service definition (or definitions).
    """
    if service_type:
        return ranger_client.get_servicedefs_by_type(service_type)
    return ranger_client.get_servicedefs()


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("configs")
def list_configs(ranger_client: RangerClient, service_type: str):
    """
    Returns `configs` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("resources")
def list_resources(ranger_client: RangerClient, service_type: str):
    """
    Returns `resources` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("accessTypes")
def list_access_types(ranger_client: RangerClient, service_type: str):
    """
    Returns `accessTypes` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("policyConditions")
def list_policy_conditions(ranger_client: RangerClient, service_type: str):
    """
    Returns `policyConditions` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("contextEnrichers")
def list_context_enrichers(ranger_client: RangerClient, service_type: str):
    """
    Returns `contextEnrichers` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("enums")
def list_enums(ranger_client: RangerClient, service_type: str):
    """
    Returns `enums` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("dataMaskDef")
def list_datamaskdef(ranger_client: RangerClient, service_type: str):
    """
    Returns `dataMaskDef` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)


@servicedef.command(context_settings=CONTEXT_SETTINGS)
@service_type_option(required=True)
@provide_ranger_client
@table_response_and_exit("rowFilterDef")
def list_rowfilterdef(ranger_client: RangerClient, service_type: str):
    """
    Returns `rowFilterDef` properties from service definitions.
    """
    return ranger_client.get_servicedefs_by_type(service_type)