import ast
import click
import pathlib
import confuse
import yaml
import functools

from ranger_cli.utils import CONTEXT_SETTINGS


def get_profile_configs(configuration: confuse.Configuration):
    return [
        {key: {conf_key: conf_value.get() 
        for conf_key, conf_value in configuration[key].items()}} 
        for key in configuration.all_contents()
    ]


def configure_configs(profile_name: str, endpoint: str, username: str, password: str, verification: str):
    profile = {}

    configuration = confuse.Configuration("ranger")
    configuration_file = pathlib.Path(configuration.user_config_path())

    if not configuration_file.exists():
        # Configuration file doesn't exist yet, create file and new profile.
        profile[profile_name] = {"endpoint": endpoint, "authentication": [username, password], "verification": ast.literal_eval(verification)}
        configuration_file.write_text(yaml.dump(profile))
        click.echo(f"Created profile '{profile_name}' in {configuration_file}.")
        return

    if configuration[profile_name].exists():
        # Profile exists, overwrite with new properties
        current_profiles = get_profile_configs(configuration)

        profile[profile_name] = {"endpoint": endpoint, "authentication": [username, password], "verification": ast.literal_eval(verification)}
        current_profiles[0].update(profile) # update profile
        profiles = functools.reduce(lambda x, y: {**x, **y}, current_profiles)
        configuration_file.write_text(yaml.dump(profiles))
        click.echo(f"Updated profile '{profile_name}' in {configuration_file}.")

    else:
        # Profile doesn't exist, add new profile
        current_profiles = get_profile_configs(configuration)

        profile[profile_name] = {"endpoint": endpoint, "authentication": [username, password], "verification": ast.literal_eval(verification)}
        current_profiles.append(profile)
        profiles = functools.reduce(lambda x, y: {**x, **y}, current_profiles)
        configuration_file.write_text(yaml.dump(profiles))
        click.echo(f"Added profile '{profile_name}' in {configuration_file}.")


def add_profile(profile: str):
    username = click.prompt("Provide your Apache Ranger REST API username")
    password = click.prompt("Provide your Apache Ranger REST API password",
                            hide_input=True,
                            confirmation_prompt=True)
    endpoint = click.prompt("Provide your Apache Ranger REST API URL with port")
    verification = click.prompt("Provide your Apache Ranger REST API SSL ca certificate", default=False)

    configure_configs(profile, endpoint, username, password, verification)


def delete_profile(profile: str):
    configuration = confuse.Configuration("ranger")
    configuration_file = pathlib.Path(configuration.user_config_path())

    if configuration_file.exists():
        if configuration[profile].exists():
            for current_profiles in get_profile_configs(configuration):
                if profile in current_profiles:
                    del current_profiles[profile]

            profiles = functools.reduce(lambda x, y: {**x, **y}, current_profiles)
            print(profiles)
            # FINISH THIS FUNCTION
            #configuration_file.write_text(yaml.dump(profiles))
            #click.echo(f"Deleted profile '{profile}' from {configuration_file}.")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("--profile", "-p", help="Profile name", default="default")
@click.option("--delete", help="Deletes profile from configuration file", is_flag=True, show_default=True, default=False)
def configure(profile: str, delete: bool):
    """
    Configures Apache Ranger REST API profiles for the CLI.
    """
    add_profile(profile) if not delete else delete_profile(profile)
