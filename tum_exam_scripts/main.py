"""
Main.
"""
from logging import INFO, basicConfig, getLogger
from typing import Optional

from tum_exam_scripts import __version__
from tum_exam_scripts.enums import Browser
from tum_exam_scripts.logic.pdf_printing import install_linux_driver_internal
from tum_exam_scripts.pdf_commands import app as pdf_commands_app
from tum_exam_scripts.shared import DRIVER_OPTION
from tum_exam_scripts.utils.password_handling import (
    get_password_from_keyring,
    store_password,
)
from tum_exam_scripts.utils.website import open_website_internal
from typer import Argument, Exit, Option, Typer, echo

_USER_ARGUMENT = Argument(
    None,
    help="The username for your informatics account, i.e., the first letters of your lastname.",
)
_LOGGER = getLogger(__name__)
basicConfig(
    format="%(levelname)s: %(asctime)s: %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=INFO,
    filename="tum-exam-scripts.log",
    filemode="a",
)


def _version_callback(value: bool) -> None:
    if value:
        echo(f"tum-exam-scripts {__version__}")
        raise Exit()


app = Typer()


@app.callback()
def _call_back(
    _: bool = Option(
        None,
        "--version",
        is_flag=True,
        callback=_version_callback,
        expose_value=False,
        is_eager=True,
        help="Version",
    )
) -> None:
    """
    A collection of useful commands to print TUMExams. You can find the source code under https://gitlab.lrz.de/i4/software/tum-exam-scripts
    """


@app.command()
def install_linux_driver(
    driver_name: str = DRIVER_OPTION,
    user_password: str = Option(
        None,
        "--password",
        "-p",
        help="Your user password. NOTE: The user should have 'sudo' privileges.",
        hide_input=True,
        prompt=True,
    ),
) -> None:
    """
    This snippet downloads the Linux driver for the printers and makes them available under $driver_name
    This is needed as the macOS driver cannot handle the booklets.
    Please change the command on mac for printing the exams from `-dfollowme` to `-dfollowmepdd`!!!
    """
    install_linux_driver_internal(driver_name, user_password)


@app.command()
def store_password_in_password_manager(
    password: str = Option(
        None,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="The password for your informatics account",
    ),
    user_name: str = _USER_ARGUMENT,
    force: bool = Option(
        False,
        "--force",
        "-f",
        is_flag=True,
        help="If true, we will overwrite existing passwords.",
    ),
) -> None:
    """
    Stores the password in the password manager.
    """
    store_password(force, password, user_name)


@app.command()
def open_printing_page(
    user_name: str = _USER_ARGUMENT,
    browser: Browser = Option(
        "firefox", "--browser", "-b", help="The browser to start."
    ),
    password: Optional[str] = Option(
        None,
        "--password",
        "-p",
        help="The password for your informatics account. If you do not pass a password, we will use the password stored in the password manager.",
    ),
) -> None:
    """
    Open the page we need to send the PDFs to the FollowMe printer.

    """
    if password is None:
        password = get_password_from_keyring(user_name)
    open_website_internal(user_name, password, browser)


app.add_typer(pdf_commands_app, name="pdf")

if __name__ == "__main__":
    app()
