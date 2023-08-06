import click
import six

from ranger_cli.cli_types import ProfileContext
from ranger_cli.utils import read_config
from ranger_cli.client import RangerClient


def provide_ranger_client(func: callable):
    """
    Injects `RangerClient` object into all wrapped callbacks; expects 
    the ``environment`` argument.
    """
    @six.wraps(func)
    def inner_wrapper(*args: list, **kwargs: dict):
        kwargs['ranger_client'] = get_profile_context()
        return func(*args, **kwargs)
    return inner_wrapper


def get_profile_context():
    ctx = click.get_current_context()
    profile_ctx = ctx.ensure_object(ProfileContext)
    profile = profile_ctx.get_profile()
    if not profile:
        raise click.UsageError("Apache Ranger public REST API profile not set")
    return RangerClient(**read_config(profile))
