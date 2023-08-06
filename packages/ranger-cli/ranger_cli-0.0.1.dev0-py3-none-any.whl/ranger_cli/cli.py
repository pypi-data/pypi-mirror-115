import click

from ranger_cli.utils import CONTEXT_SETTINGS
from ranger_cli.policy.commands import policy
from ranger_cli.service.commands import service
from ranger_cli.configure.commands import configure
from ranger_cli.servicedef.commands import servicedef
from ranger_cli.plugins.commands import plugins
from ranger_cli.version import version


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version)
def cli():
    """
    Welcome to the (unofficial) Apache Ranger public REST API command-line interface!

    Docs:    https://python-ranger.readthedocs.io
    PyPI:    https://pypi.org/project/python-ranger
    GitHub:  https://github.com/degagne/python-ranger
    """
    pass


cli.add_command(configure)
cli.add_command(policy)
cli.add_command(service)
cli.add_command(servicedef)
cli.add_command(plugins)


if __name__ == "__main__":
    cli()
