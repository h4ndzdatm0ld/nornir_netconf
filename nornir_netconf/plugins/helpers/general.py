"""General Helpers."""
from pathlib import Path


def check_file(file_name):
    """Check file_name exists based on input."""
    try:
        file_path = Path(file_name)
        return file_path.exists()
    except TypeError:
        return False
