"""
Utils.
"""
import subprocess  # NOTE: Keep for mock/testing
from logging import getLogger
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List, Sequence

from click import echo, style
from click.exceptions import Exit

import typer  # NOTE: Keep for mock/testing
from typer.colors import RED

_LOGGER = getLogger(__name__)


def error_echo(s: str) -> None:
    """

    :param s:
    :return:
    """
    echo(style(s, fg=RED), err=True)


def call_command(current_file: Path, current_command: Sequence[str]) -> None:
    """
    Call a command and exits on failure.
    :param current_file:
    :param current_command:
    :return:
    """
    _LOGGER.info("Calling ...")
    _LOGGER.info(" ".join(current_command))
    _LOGGER.info("Done!")
    res = subprocess.check_call(current_command)
    if res != 0:
        error_echo(f"Something went wrong when sending {current_file} to the server")
        error_echo(f"Please open a shell and call {' '.join(current_command)}")
        raise Exit(1)


def confirm_printing_rights() -> None:
    """
    Ask the user whether they have enabled the printing.
    """
    if not typer.confirm(
        "Did you enable printing from your PC via https://ucentral.in.tum.de/cgi-bin/printman.cgi ?"
    ):
        echo("Please enable printing first!")
        raise Exit


def sudo_call(command: List[str], password: str) -> None:
    """
    Sudo call.
    """
    changed_command = ["sudo", "-S"] + command
    _LOGGER.info("Calling ...")
    _LOGGER.info(" ".join(changed_command))
    _LOGGER.info("Done!")
    proc = Popen(
        changed_command,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    proc.communicate(password.encode())
    if proc.returncode != 0:
        error_echo("Installation went wrong.")
        error_echo(f"Please open a shell and call 'sudo {' '.join(command)}'")
        raise Exit(1)
