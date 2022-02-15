"""
Main.
"""

from logging import INFO, basicConfig, getLogger
from os import remove
from pathlib import Path
from tempfile import gettempdir
from typing import List
from urllib.request import urlretrieve

from tum_exam_scripts import __version__
from tum_exam_scripts.utils import (
    send_pdf_files, call_command,
    confirm_printing_rights,
    sudo_call,
)
from typer import Exit, Option, Typer, echo

_DRIVER_OPTION = Option("followmeppd", "--driver-name", "-d", help="Name of the driver")

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

    :return:
    """


@app.command()
def install_linux_driver(
    driver_name: str = _DRIVER_OPTION,
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
    tempdir = Path(gettempdir())
    local_file = tempdir.joinpath("x2UNIV.ppd")
    urlretrieve(
        "https://wiki.in.tum.de/foswiki/pub/Informatik/Benutzerwiki/XeroxDrucker/x2UNIV.ppd",
        str(local_file),
    )
    sudo_call(
        [
            "lpadmin",
            "-E",
            "-p",
            driver_name,
            "-v",
            "ipps://print.in.tum.de/printers/followme",
            "-P",
            str(local_file),
            "-D",
            "Xerox-Followme",
            "-L",
            "TUM",
        ],
        user_password,
    )
    sudo_call(["cupsenable", driver_name], user_password)
    sudo_call(["cupsaccept", driver_name], user_password)
    remove(local_file)


@app.command()
def send_all_booklets(
    driver_name: str = _DRIVER_OPTION,
    input_directory: Path = Option(
        ".",
        "--input-directory",
        "-d",
        exists=True,
        resolve_path=True,
        help="The directory with the exams from the TUMExam website.",
        file_okay=False,
    ),
) -> None:
    """
    Send all booklets to the printing server.

    Example:
        tum-exam-scripts send-all-booklets --input-directory /path/to/exams/
    """
    confirm_printing_rights()
    pdf_files = sorted(input_directory.glob("*-book.pdf"))
    if len(pdf_files) == 0:
        echo(f"We did not find any booklets. Please check {input_directory}")
        raise Exit(1)
    echo(f"We found {len(pdf_files)} booklets.")
    send_pdf_files(driver_name, pdf_files)


@app.command()
def send_specific_booklets(
    pdf_file: List[Path] = Option(
        [],
        "--booklet-pdf",
        "-P",
        exists=True,
        resolve_path=True,
        help="The directory with the exams from the TUMExam website.",
        dir_okay=False,
    ),
    driver_name: str = _DRIVER_OPTION,
) -> None:
    """
    Send only specific PDFs to the server. You can pass multiple files.

    Example:
        tum-exam-scripts send-specific-booklets --booklet-pdf /path/to/E0007-book.pdf --booklet-pdf /path/to/E0009-book.pdf
    """
    confirm_printing_rights()
    send_pdf_files(driver_name, pdf_file)


@app.command()
def send_attendee_list(
    attend_list: Path = Option(
        "attendeelist.pdf",
        "--attendee-list",
        "-a",
        exists=True,
        resolve_path=True,
        help="The directory with the exams from the TUMExam website.",
        dir_okay=False,
    ),
    driver_name: str = _DRIVER_OPTION,
) -> None:
    """
    Send the attendee list to the server.

    Example:
        tum-exam-scripts send-attendee-list --attendee-list /path/to/attendeelist.pdf
    """
    confirm_printing_rights()
    echo(f"Sending document {attend_list} to the printing server ...")
    current_command = [
        "lp",
        "-d" + driver_name,
        "-o",
        "PageSize=A4",
        "-o",
        "JCLBanner=False",
        "-o",
        "JCLColorCorrection=PressMatch",
        "-o",
        "Duplex=None",
        "-o",
        "JCLPrintQuality=Enhanced",
        "-o",
        "InputSlot=ManualFeed",
        "-o",
        "MediaType=Labels",
        str(attend_list),
    ]
    call_command(attend_list, current_command)


if __name__ == "__main__":
    app()
