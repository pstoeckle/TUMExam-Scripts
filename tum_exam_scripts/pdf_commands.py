"""
PDF commands.
"""
from pathlib import Path
from typing import List, Optional

from click import echo
from click.exceptions import Exit

from tum_exam_scripts.logic.pdf_printing import (
    send_attendee_list_internal,
    send_pdf_files,
)
from tum_exam_scripts.shared import DRIVER_OPTION
from tum_exam_scripts.utils.command import call_command, confirm_printing_rights
from typer import Argument, Option, Typer

app = Typer()


@app.callback()
def _call_back() -> None:
    """
    Subgroup with the PDF printing commands.
    """


@app.command()
def send_all_booklets(
    driver_name: str = DRIVER_OPTION,
    input_directory: Path = Argument(
        ".",
        exists=True,
        resolve_path=True,
        help="The directory with the exams from the TUMExam website.",
        file_okay=False,
    ),
    batch_size: Optional[int] = Option(
        None,
        "--batch-size",
        "-b",
        help="If you add a batch size, the process will stop after so many exams and wait for you to continue."
        "You can you this so start all jobs on a printer, then send the next batch, and start these exams on another printer.",
    ),
) -> None:
    """
    Send all booklets to the printing server.

    Example:
        tum-exam-scripts send-all-booklets /path/to/exams/
    """
    if batch_size is not None:
        if batch_size < 2:
            echo(f"{batch_size} is not a valid batch size!")
            raise Exit(1)
    confirm_printing_rights()
    pdf_files = sorted(input_directory.glob("*-book.pdf"))
    if len(pdf_files) == 0:
        echo(f"We did not find any booklets. Please check {input_directory}")
        raise Exit(1)
    echo(f"We found {len(pdf_files)} booklets.")
    send_pdf_files(driver_name, pdf_files, batch_size)


@app.command()
def send_specific_booklets(
    pdf_file: List[Path] = Argument(
        None,
        exists=True,
        resolve_path=True,
        help="The directory with the exams from the TUMExam website.",
        dir_okay=False,
    ),
    driver_name: str = DRIVER_OPTION,
) -> None:
    """
    Send only specific PDFs to the server. You can pass multiple files.

    Example:
        tum-exam-scripts send-specific-booklets /path/to/E0007-book.pdf /path/to/E0009-book.pdf
    """
    confirm_printing_rights()
    send_pdf_files(driver_name, pdf_file)


@app.command()
def send_attendee_list(
    attend_list: Path = Argument(
        "attendeelist.pdf",
        exists=True,
        resolve_path=True,
        help="The attendee list from the TUMExam endterm_lists folder.",
        dir_okay=False,
    ),
    driver_name: str = DRIVER_OPTION,
) -> None:
    """
    Send the attendee list to the server.

    Example:
        tum-exam-scripts send-attendee-list /path/to/attendeelist.pdf
    """
    confirm_printing_rights()
    send_attendee_list_internal(attend_list, driver_name)


@app.command()
def send_seat_plan(
    seat_plan: Path = Argument(
        "seatplan-a3.pdf",
        exists=True,
        resolve_path=True,
        help="The seat plan in A3 from the TUMExam endterm_lists folder.",
        dir_okay=False,
    ),
    driver_name: str = DRIVER_OPTION,
    versions: int = Option(
        3, "--number-of-copies", "-n", help="The number of copies you want to print."
    ),
) -> None:
    """
    Print the seat plans in A3. You have to put them at the doors of the lecture hall.
    """
    confirm_printing_rights()
    echo(f"Sending document {seat_plan} to the printing server ...")
    current_command = [
        "lp",
        "-d" + driver_name,
        "-n",
        str(versions),
        "-o",
        "PageSize=A3",
        "-o",
        "JCLBanner=False",
        "-o",
        "JCLColorCorrection=BlackWhite",
        "-o",
        "Duplex=None",
        "-o",
        "JCLPrintQuality=Enhanced",
        str(seat_plan),
    ]
    call_command(seat_plan, current_command)


@app.command()
def send_room_layout(
    room_plan: Path = Argument(
        "roomplan.pdf",
        exists=True,
        resolve_path=True,
        help="The room plan in A3 from the TUMExam endterm_lists folder.",
        dir_okay=False,
    ),
    driver_name: str = DRIVER_OPTION,
    versions: int = Option(
        3, "--number-of-copies", "-n", help="The number of copies you want to print."
    ),
) -> None:
    """
    Print the room plans in A3. You have to put them at the doors of the lecture hall.
    """
    confirm_printing_rights()
    echo(f"Sending document {room_plan} to the printing server ...")
    current_command = [
        "lp",
        "-d" + driver_name,
        "-n",
        str(versions),
        "-o",
        "PageSize=A3",
        "-o",
        "JCLBanner=False",
        "-o",
        "JCLColorCorrection=PressMatch",
        "-o",
        "Duplex=None",
        "-o",
        "JCLPrintQuality=Enhanced",
        str(room_plan),
    ]
    call_command(room_plan, current_command)
