"""General Helpers."""
import logging
import os.path
from pathlib import Path


def check_file(file_name: str) -> bool:
    """Check file_name exists based on input.

    Args:
        file_name (str): file name to check
    """
    try:
        file_path = Path(file_name)
        return file_path.exists()
    except TypeError:
        return False


def create_folder(directory: str) -> None:
    """Create a directory.

    Args:
        directory (str): Directory path to create
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as err_ex:
        logging.info("Error when creating %s, %s", directory, err_ex)


def write_output(text: str, path: str, filename: str) -> None:
    """Take input and path and write a file.

    Args:
        text (str): text to write
        path (str): directory path
        filename (str): filename
    """
    if not os.path.isdir(path):
        create_folder(path)
    with open(f"{path}/{filename}.txt", "w+", encoding="utf-8") as file:
        file.write(str(text))
