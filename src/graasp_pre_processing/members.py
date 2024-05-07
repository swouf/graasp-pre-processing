from io import TextIOWrapper
import pandas as pd
from pathlib import Path


def parse_members(filehandler: TextIOWrapper) -> pd.DataFrame:
    data = pd.read_json(filehandler)
    return data

def parse_members_from_file(
    path,
) -> pd.DataFrame:
    """
    docstring
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_members(openedFile)