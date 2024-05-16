from io import TextIOWrapper
import pandas as pd
from pathlib import Path


def parse_descendants(filehandler: TextIOWrapper) -> pd.DataFrame:
    data = pd.read_json(filehandler)
    return data


def parse_descendants_from_file(
    path,
) -> pd.DataFrame:
    """
    docstring
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_descendants(openedFile)
