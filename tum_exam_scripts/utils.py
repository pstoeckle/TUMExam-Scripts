"""
Utils.
"""
import subprocess  # NOTE: Keep for mock/testing
from logging import getLogger
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List, Optional, Sequence

from click import echo, pause, style
from click.exceptions import Exit
from tqdm import tqdm

import typer  # NOTE: Keep for mock/testing
from tum_exam_scripts.pdf_utils import is_full_pdf
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


def send_pdf_files(
    driver_name: str, pdf_files: List[Path], batch_size: Optional[int] = None
) -> None:
    """
    Send all PDF files to the server.
    :param batch_size:
    :param driver_name:
    :param pdf_files:
    :return:
    """
    echo("Check whether PDFs are corrupt")
    for pdf_file in tqdm(pdf_files):
        if not is_full_pdf(pdf_file):
            error_echo(f"The PDF file {pdf_file} is not a valid PDF.")
            raise Exit(1)
    batch_no = 0
    for i, pdf_file in enumerate(tqdm(pdf_files)):
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
        call_command(pdf_file, current_command)
        if batch_size is not None and ((i + 1) % batch_size) == 0:
            pause(f"We finished batch {batch_no}")
            batch_no += 1

    echo("Done!")
