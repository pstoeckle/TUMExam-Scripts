"""
PDF utils.
"""
from logging import getLogger
from os import remove
from os.path import getsize
from pathlib import Path
from tempfile import gettempdir
from typing import List, Optional
from urllib.request import urlretrieve

from click import echo, pause
from click.exceptions import Exit
from tqdm import tqdm

from tum_exam_scripts.utils.command import call_command, error_echo, sudo_call

_LOGGER = getLogger(__name__)


def is_full_pdf(current_file: Path) -> bool:
    """
    Check whether a file is a valid PDF.
    :param current_file:
    :return:
    """
    size = getsize(current_file)
    if size < 1024:
        return False
    with current_file.open("rb") as fin:
        # start content
        fin.seek(0)
        start_content = fin.read(1024).decode("ascii", "ignore")
        fin.seek(-1024, 2)
        end_content = fin.read().decode("ascii", "ignore")
    start_flag = False
    # %PDF
    if start_content.count("%PDF") > 0:
        start_flag = True

    if end_content.count("%%EOF") and start_flag > 0:
        return True
    eof: str = bytes([0]).decode("ascii")
    if end_content.endswith(eof) and start_flag:
        return True
    return False


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


def install_linux_driver_internal(driver_name: str, user_password: str) -> None:
    tempdir = Path(gettempdir())
    local_file = tempdir.joinpath("x2UNIV.ppd")
    _LOGGER.info("Download PPD file")
    urlretrieve(
        "https://wiki.in.tum.de/foswiki/pub/Informatik/Benutzerwiki/XeroxDrucker/x2UNIV.ppd",
        str(local_file),
    )
    _LOGGER.info("Success!")
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
    echo("The Linux driver was successfully installed!")
    remove(local_file)
    sudo_call(["cupsenable", driver_name], user_password)
    sudo_call(["cupsaccept", driver_name], user_password)
    echo(f"The printing service is available under {driver_name}")


def send_attendee_list_internal(attend_list: Path, driver_name: str) -> None:
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
