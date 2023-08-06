import click
import json

from ranger_cli.utils import CONTEXT_SETTINGS, response_and_exit, pretty_response
from ranger_cli.config import provide_ranger_client
from ranger_cli.client import RangerClient
from ranger_cli.cli_options import profile_option, service_name_option, apptype_option, hostname_option


@click.group(context_settings=CONTEXT_SETTINGS)
@profile_option()
def plugins():
    """
    Provides access Apache Ranger's plugins public REST API.
    """
    pass


@plugins.command(context_settings=CONTEXT_SETTINGS)
@apptype_option(mutually_exclusive=["hostname","service_name"])
@hostname_option(mutually_exclusive=["apptype","service_name"])
@service_name_option(mutually_exclusive=["hostname", "apptype"])
@provide_ranger_client
@response_and_exit
def info(ranger_client: RangerClient, apptype: str, hostname: str, service_name: str):
    """
    Gets all Apache Ranger plugins info.
    """
    try:
        response = ranger_client.get_plugins_info()
        response = json.loads(response)
        response = response["rangerPluginInfoes"]["rangerPluginInfo"]
    except KeyError:
        pass
    else:
        if apptype:
            return pretty_response([
                plugin
                for plugin in response 
                    if plugin.get("appType") == apptype
            ])
        elif hostname:
            return pretty_response([
                plugin
                for plugin in response
                    if plugin.get("hostName") == hostname
            ])
        elif service_name:
            return pretty_response([
                plugin
                for plugin in response
                    if plugin.get("serviceName") == service_name
            ])
