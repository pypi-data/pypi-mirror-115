import json
import time
from typing import Any, Dict, Optional

import click

from .env_constants import CONFIG_FILE
from .errors import CorruptedConfigFile


def _get_config(path: str = CONFIG_FILE) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r") as conf_file:
            return json.load(conf_file)
    except FileNotFoundError:
        return None
    except Exception as exc:
        if isinstance(exc, json.JSONDecodeError) and not exc.doc:
            # File exists, but is empty
            return None
        raise CorruptedConfigFile(path=path) from exc


def get_config(path: str = CONFIG_FILE) -> Optional[Dict[str, Any]]:
    """Get configuration from the config file. Returns None if there is no config file or it's empty."""
    try:
        return _get_config(path)
    except CorruptedConfigFile as exc:
        click.secho(
            "The Levo configuration file appears to be corrupted. "
            f"Please remove the file: {exc.path} and try again.",
            fg="red",
        )
        raise click.exceptions.Exit(1)


def get_auth_config(path: str = CONFIG_FILE) -> Optional[Dict[str, Any]]:
    """Get Auth configuration from the config file. Returns None if there is no config file or token is invalid."""
    config = get_config(path)
    if config and "auth" in config and config["auth"]["expiry"] > time.time():
        return config["auth"]
    return None


def try_get_auth_config() -> Dict[str, Any]:
    auth_config = get_auth_config()
    if not auth_config:
        click.secho(
            'You are not authenticated yet with Levo. Please login with "levo login" first.',
            fg="green",
        )
        raise click.exceptions.Exit(1)
    return auth_config
