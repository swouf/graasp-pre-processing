from io import TextIOWrapper
import logging
import pandas as pd
from pathlib import Path

log = logging.getLogger(__name__)

def get_parent_id(path: list[str]) -> str:
    try:
        return path[-2]
    except IndexError as e:
        log.warning(e, exc_info=True)
    return pd.NA

def parse_path(path: str) -> list[str]: # TODO: move to utils
    split_path = path.split('.')
    parsed_paths = list(map(lambda x: x.replace('_', '-'), split_path))
    return parsed_paths

def extract_parent_item(data: pd.DataFrame) -> pd.DataFrame:
    paths = data['path']
    parsed_paths = paths.apply(parse_path)
    parent_ids = parsed_paths.apply(get_parent_id).rename('parentId')
    return data.join(parent_ids)
    

def parse_descendants(filehandler: TextIOWrapper) -> pd.DataFrame:
    data = pd.read_json(filehandler)
    data = data.set_index('id')
    data = extract_parent_item(data)
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
