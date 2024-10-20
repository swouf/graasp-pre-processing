import argparse
from io import TextIOWrapper
import pandas as pd
from pathlib import Path
import logging

from graasp_pre_processing.apps.expand_data import (
    expand_app_data,
    expand_app_actions,
    expand_app_settings,
)

log = logging.getLogger(__name__)


def remove_item(piece_of_data):
    item = piece_of_data.pop("item", None)
    piece_of_data["itemId"] = item["id"]
    return piece_of_data


def filter_item_out(data_raw: list):
    return list(map(remove_item, data_raw))


def get_url_from_item(item):
    url = ""
    try:
        url = item["extra"]["app"]["url"]
    except KeyError as e:
        log.warning(e)
    return url


def transform_creator_to_id(data: pd.DataFrame):
    creatorId = ""
    try:
        creatorId = data["creator"].apply(lambda x: x["id"]).rename("creatorId")
    except KeyError as e:
        log.warning(e)
    return data.join(creatorId)


def parse_actions(actions_raw, item):
    url = get_url_from_item(item)
    actions = expand_app_actions(actions_raw, url)
    return actions


def parse_data(app_data_raw: list, item) -> pd.DataFrame:
    log.debug("Type of app_data_raw: %s", str(type(app_data_raw)))
    url = get_url_from_item(item)
    app_data = expand_app_data(filter_item_out(app_data_raw), url)
    app_data = transform_creator_to_id(app_data)
    return app_data


def parse_settings(settings_raw: list, item: dict) -> tuple[pd.DataFrame | None, dict]:
    url = get_url_from_item(item)
    app_settings = expand_app_settings(filter_item_out(settings_raw), url)
    log.debug("App settings expanded.")
    return app_settings, item

def parse_app_row(row: pd.Series):
    item = {}
    for app_state_list in [row["settings"], row["actions"], row["data"]]:
      if len(app_state_list) > 0:
        item = app_state_list[0]["item"]
        break
    app_settings, item = parse_settings(row["settings"], item)
    app_actions = parse_actions(row["actions"], item)
    app_data = parse_data(row["data"], item)

    itemDf = pd.DataFrame(
        [pd.Series(item)],
        columns=[
            "id",
            "name",
            "displayName",
            "description",
            "type",
            "createdAt",
            "updatedAt",
            "deletedAt",
            "extra",
            "settings",
            "path",
            "lang",
        ],
    )
    log.debug("Item dataframe:\n%s", itemDf)

    return pd.Series(
        {
            "app-data": app_data,
            "app-settings": app_settings,
            "app-actions": app_actions,
            "item": itemDf,
        }
    )


def parse_apps_data(
    filehandler: TextIOWrapper,
) -> pd.DataFrame:
    """
    Parse multiple apps data from an already opened file.
    """
    data = pd.read_json(filehandler, orient="index")
    data = data.apply(parse_app_row, axis="columns")

    return data


def parse_apps_data_from_file(
    path,
) -> pd.DataFrame:
    """
    docstring
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_apps_data(openedFile)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    parse_apps_data_from_file(args.filename)
