"""
PDF utils.
"""
from os.path import getsize
from pathlib import Path


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
