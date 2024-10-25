from io import TextIOWrapper
import pandas as pd
from pathlib import Path

from pandera import check_output

from graasp_pre_processing.entities.schemas import members_schema

@check_output(members_schema)
def parse_members(filehandler: TextIOWrapper) -> pd.DataFrame:
    data = pd.read_json(filehandler)
    data = data.set_index("id")
    return data


def parse_members_from_file(
    path,
) -> pd.DataFrame:
    """
    Open and parse members data from Graasp dump.
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_members(openedFile)
