"""
Main.
"""
from logging import INFO, basicConfig, getLogger
from os import remove
from pathlib import Path
from subprocess import PIPE, Popen, check_call
from tempfile import gettempdir
from typing import List
from urllib.request import urlretrieve

from tqdm import tqdm

from tum_exam_scripts import __version__
from typer import Exit, Option, Typer, confirm, echo, style
from typer.colors import RED

_DRIVER_OPTION = Option("followmeppd", "--driver-name", "-d", help="Name of the driver")


_LOGGER = getLogger(__name__)
basicConfig(
    format="%(levelname)s: %(asctime)s: %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=INFO,
    filename="tum-exam-scripts.log",
    filemode="a",
)


def error_echo(s: str) -> None:
    """

    :param s:
    :return:
    """
    echo(style(s, fg=RED), err=True)


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
    _sudo_call(
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
    _sudo_call(["cupsenable", driver_name], user_password)
    _sudo_call(["cupsaccept", driver_name], user_password)
    remove(local_file)


def _sudo_call(command: List[str], password: str) -> None:
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
    _confirm_printing_rights()
    pdf_files = sorted(input_directory.glob("*-book.pdf"))
    if len(pdf_files) == 0:
        echo(f"We did not find any booklets. Please check {input_directory}")
        raise Exit(1)
    echo(f"We found {len(pdf_files)} booklets.")
    _send_pdf_files(driver_name, pdf_files)


def _confirm_printing_rights() -> None:
    if not confirm(
        "Did you enable printing from your PC via https://ucentral.in.tum.de/cgi-bin/printman.cgi ?"
    ):
        echo("Please enable printing first!")
        raise Exit


def _send_pdf_files(driver_name: str, pdf_files: List[Path]) -> None:
    for pdf_file in tqdm(pdf_files):
        echo(f"Sending document {pdf_file} to the printing server ...")
        current_command = [
            "lp",
            "-d" + driver_name,
            "-o",
            "PageSize=A3",
            "-o",
            "JCLBanner=False",
            "-o",
            "JCLColorCorrection=BlackWhite",
            "-o",
            "Duplex=DuplexNoTumble",
            "-o",
            "XRFold=BiFoldStaple",
            "-o",
            "landscape",
            "-o",
            "JCLPrintQuality=Enhanced",
            str(pdf_file),
        ]
        _LOGGER.info("Calling ...")
        _LOGGER.info(" ".join(current_command))
        _LOGGER.info("Done!")
        res = check_call(current_command)
        if res != 0:
            error_echo(f"Something went wrong when sending {pdf_file} to the server")
            error_echo(f"Please open a shell and call {' '.join(current_command)}")
            raise Exit(1)
    echo("Done!")


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
    _confirm_printing_rights()
    _send_pdf_files(driver_name, pdf_file)


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
    _confirm_printing_rights()
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
    _LOGGER.info("Calling ...")
    _LOGGER.info(" ".join(current_command))
    _LOGGER.info("Done!")
    res = check_call(current_command)
    if res != 0:
        error_echo(f"Something went wrong when sending {attend_list} to the server")
        error_echo(f"Please open a shell and call {' '.join(current_command)}")
        raise Exit(1)


if __name__ == "__main__":
    app()
