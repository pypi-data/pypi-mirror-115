"""The login module which maintains the authentication logic."""

import datetime
import json
import os
import os.path
import time
import webbrowser
from pathlib import Path

import click
import requests

from .config_file import get_config
from .env_constants import (
    CONFIG_FILE,
    DAF_AUDIENCE,
    DAF_CLIENT_ID,
    DAF_DOMAIN,
    DAF_GRANT_TYPE,
    DAF_SCOPES,
)


def get_api_token(device_code):
    """Given the device_code, gets the API token from Device Authorization Flow server."""
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": DAF_GRANT_TYPE,
        "device_code": device_code,
        "client_id": DAF_CLIENT_ID,
    }
    response = requests.post(DAF_DOMAIN + "/oauth/token", headers=headers, data=data)
    return response.json()


def _augment_access_token(access_token):
    """Add additional attributes to the access token provided by IAM provider"""
    access_token["expiry"] = time.time() + access_token["expires_in"]


def _write_token_to_config_file(token):
    if not isinstance(token, dict):
        return

    if not os.path.exists(os.path.dirname(CONFIG_FILE)):
        Path(os.path.dirname(CONFIG_FILE)).mkdir(
            mode=0o700, parents=True, exist_ok=True
        )

    config = get_config()

    # Write the tokens back to the file with 0600 permissions
    try:
        conf_fd = os.open(
            CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o600
        )
        with os.fdopen(conf_fd, "w") as config_file:
            if config is None:
                config = {}
            config.setdefault("config_version", "1.0.0")
            config.setdefault("auth", {})
            config["auth"].update(token)
            json.dump(config, config_file, indent=2)
    except OSError:
        click.secho(
            f"Cannot write config to file {CONFIG_FILE}",
            fg="red",
        )
        raise click.exceptions.Exit(1)


def _is_current_access_token_valid():
    """Checks if the persisted access token is still valid and not expired"""
    config = get_config()
    if config is None:
        return False

    if "auth" not in config or "access_token" not in config["auth"]:
        return False

    auth_info = config["auth"]
    if "refresh_token" in auth_info and "expiry" in auth_info:
        if auth_info["expiry"] > time.time():
            return True

    # If we get here, we need to refresh our access token
    token = refresh_access_token(auth_info["refresh_token"])
    if token:
        _augment_access_token(token)
        _write_token_to_config_file(token)
        return True

    return False


def login_with_browser():
    """Signup/Login to Levo service using the browser."""
    # Request device code
    payload = {
        "client_id": DAF_CLIENT_ID,
        "scope": DAF_SCOPES,
        "audience": DAF_AUDIENCE,
    }
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        DAF_DOMAIN + "/oauth/device/code", headers=headers, data=payload
    )
    # Storing device verification details: https://auth0.com/docs/api/authentication#get-device-code
    device = response.json()

    # Setup timeout and interval based on auth0 response
    timeout = time.time() + device["expires_in"]
    interval = device["interval"]

    # Ask for user interaction to activate the device
    click.secho("👋 Welcome to Levo! Please follow the steps to authenticate.")
    click.echo()
    click.secho(
        "Your device code is: {user_code}.".format(user_code=device["user_code"]),
        fg="green",
    )
    click.echo()
    click.secho("Please verify this CLI device by navigating here: ", nl=False)
    click.secho(device["verification_uri_complete"], fg="bright_blue", underline=True)
    click.echo()

    # Open the login screen in the browser
    webbrowser.open_new(device["verification_uri_complete"])

    # Keep polling to see if the authentication is done.
    last_time = time.time()
    success = False
    while last_time < timeout:
        remaining_time = (
            str(datetime.timedelta(seconds=(timeout - last_time)))
            .split(":", 1)[1]
            .rsplit(".", 1)[0]
        )
        click.secho(
            "Waiting for device verification... verification will expire in "
            + remaining_time
            + "\r",
            nl=False,
        )
        token = get_api_token(device["device_code"])

        # If access token is present verification was successful
        if "access_token" in token:
            _augment_access_token(token)
            _write_token_to_config_file(token)
            click.echo()
            click.secho(
                "\nYour account has been authenticated. Levo is now ready to be used!",
                fg="green",
            )
            success = True
            break
        time.sleep(interval - (time.time() - last_time))
        last_time = time.time()
    # Let the user know when verification fails.
    if not success:
        click.echo()
        click.secho(
            "Your device verification process has expired. Please try to login again.",
            fg="red",
        )


def refresh_access_token(refresh_token):
    """Refresh the API access token with the given refresh token."""
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": DAF_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    response = requests.post(DAF_DOMAIN + "/oauth/token", headers=headers, data=data)
    if response.status_code == 200:
        click.secho("Refreshed the access token with Levo.", fg="green")
        return response.json()

    return  # None


def login_or_refresh():
    """Authenticate with Levo. If there is a valid token that's not expired yet,
    this will not do anything.
    """
    if _is_current_access_token_valid():
        click.secho(
            "Your account has been authenticated. Levo is now ready to be used!",
            fg="green",
        )
    else:
        login_with_browser()  # Else login now and get the api_token

    return
