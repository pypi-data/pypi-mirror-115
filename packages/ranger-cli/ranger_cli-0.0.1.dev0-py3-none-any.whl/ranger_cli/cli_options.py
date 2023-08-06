import click
import pathlib

from ranger_cli.cli_types import MutuallyExclusiveOption
from ranger_cli.cli_types import ProfileContext
from ranger_cli.utils import get_default_profile


class MutuallyExclusiveOptionBase:
    """
    Base class for `click.Option` objects with support for 'mutually exclusive' arguments.
    """

    def __init__(self, mutually_exclusive: list, required: bool):
        self.mutually_exclusive = mutually_exclusive
        self.required = required

    def callback(self, ctx: click.Context, param: click.Option, value: str):
        ctx_obj = ctx.ensure_object(dict)
        if ctx_obj is not None:
            ctx_obj[param] = value
        return value


class OptionBase:
    """
    Base class for `click.Option` objects.
    """

    def __init__(self, required: bool):
        self.required = required

    def callback(self, ctx: click.Context, param: click.Option, value: str):
        ctx_obj = ctx.ensure_object(dict)
        if ctx_obj is not None:
            ctx_obj[param] = value
        return value


class FileBase:
    """
    Base class for `click.Option` objects with file support.
    """

    def __init__(self, required: bool):
        self.required = required

    def callback(self, ctx: click.Context, param: click.Option, value: str):
        ctx_obj = ctx.ensure_object(dict)
        if ctx_obj is not None:
            ctx_obj[param] = value
        return pathlib.Path(value).expanduser().read_text()


class profile_option:
    """
    CLI option `--profile`.

    Apache Ranger public REST API profile name with default being the first profile
    found in the YAML configuration file.
    """

    def __init__(self, required=False):
        self.required = required

    def __call__(self, func):
        def _callback(ctx: click.Context, param: str, value: str):
            profile_ctx = ctx.ensure_object(ProfileContext)
            profile_ctx.set_profile(value)

        return click.option("--profile", "-p",
                            help=f"Apache Ranger public REST API profile name (default='{get_default_profile()}').",
                            default=get_default_profile(),
                            callback=_callback,
                            expose_value=False,
                            required=self.required)(func)


class policy_id_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--policy-id`.

    Apache Ranger resource-based policy id.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--policy-id", "-i", 
                            help="Apache Ranger resource-based policy id.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)


class policy_name_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--policy-name`.

    Apache Ranger resource-based policy name.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--policy-name", "-n",
                            help="Apache Ranger resource-based policy name.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)


class service_name_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--service-name`.

    Apache Ranger service repository name.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--service-name", "-s",
                            help="Apache Ranger service repository name.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)


class service_id_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--service-id`.

    Apache Ranger service repository id.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--service-id", "-S",
                            help="Apache Ranger service repository id.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)


class config_option(FileBase):
    """
    CLI option `--config`.

    Configuration file containing resource properties.
    """

    def __init__(self, required=False):
        super().__init__(required)

    def __call__(self, func):
        return click.option("--config",
                            help="Configuration file containing resource properties.",
                            type=click.Path(exists=True),
                            callback=self.callback,
                            required=self.required)(func)


class service_type_option(OptionBase):
    """
    CLI option `--service-type`.

    Apache Ranger servicedef REST API service types
    """

    def __init__(self, required=False):
        super().__init__(required)
        self.options = ["hdfs", "hive", "hbase", "knox", "storm", "solr", "kafka", "yarn", "atlas", "kms", "nifi"]

    def __call__(self, func):
        return click.option("--service-type", "-t",
                            help=f"Apache Ranger servicedef REST API service types.",
                            type=click.Choice(self.options, case_sensitive=False),
                            callback=self.callback,
                            required=self.required)(func)


class apptype_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--apptype`.

    Apache Ranger application type.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--apptype", "-a",
                            help="Apache Ranger application type.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)


class hostname_option(MutuallyExclusiveOptionBase):
    """
    CLI option `--hostname`.

    Apache Ranger application type.
    """

    def __init__(self, mutually_exclusive: list = [], required=False):
        super().__init__(mutually_exclusive, required)

    def __call__(self, func):
        return click.option("--hostname", "-n",
                            help="Apache Ranger hostname.",
                            cls=MutuallyExclusiveOption,
                            mutually_exclusive=self.mutually_exclusive,
                            callback=self.callback,
                            required=self.required)(func)