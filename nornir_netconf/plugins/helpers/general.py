"""General Helpers."""
import os.path
from pathlib import Path


def check_file(file_name):
    """Check file_name exists based on input."""
    try:
        file_path = Path(file_name)
        return file_path.exists()
    except TypeError:
        return False


def write_output(text: str, path: str):
    """Take input and path and write a file.

    Args:
        text (str): [description]
        path (str): [description]
    """
    if not os.path.isdir(path):
        raise TypeError(f"{path} is not a valid directory.")
    with open(path, "w+", encoding="utf-8") as file:
        file.write(text)
