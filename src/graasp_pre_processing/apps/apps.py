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


def parse_actions(actions_raw, item):
    url = ""
    try:
        url = item["extra"]["app"]["url"]
    except KeyError as e:
        log.warning(e)
    actions = expand_app_actions(actions_raw, url)
    return actions


def parse_data(app_data_raw: list, item) -> pd.DataFrame:
    log.debug("Type of app_data_raw: %s", str(type(app_data_raw)))
    url = ""
    try:
        url = item["extra"]["app"]["url"]
    except KeyError as e:
        log.warning(e)
    app_data = expand_app_data(filter_item_out(app_data_raw), url)
    creatorId = ""
    try:
        creatorId = app_data["creator"].apply(lambda x: x["id"]).rename("creatorId")
    except KeyError as e:
        log.warning(e)
    app_data = app_data.join(creatorId)
    return app_data


def parse_settings(settings_raw: list) -> tuple[pd.DataFrame | None, dict]:
    item = {}
    url = ""
    if len(settings_raw) > 0:
        item = settings_raw[0]["item"]
        log.debug("Item: %s", item)
        url = ""
        try:
            url = item["extra"]["app"]["url"]
        except KeyError as e:
            log.warning(e)
    app_settings = expand_app_settings(filter_item_out(settings_raw), url)
    log.debug("App settings expanded.")
    return app_settings, item


def parse_app_row(row: pd.Series):
    app_settings, item = parse_settings(row["settings"])
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
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse multiple apps data from an already opened file.
    """
    data = pd.read_json(filehandler, orient="index")
    data = data.apply(parse_app_row, axis="columns")

    app_data = pd.concat(data["app-data"].values)
    app_actions = pd.concat(data["app-actions"].values)
    app_settings = pd.concat(data["app-settings"].values)
    items = pd.concat(data["item"].values).set_index("id")

    return app_data, app_actions, app_settings, items


def parse_apps_data_from_file(
    path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    docstring
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_apps_data(openedFile)


if __name__ == "__main__":
    # from pyproject_parser import PyProject
    # project = PyProject()
    # project.load("pyproject.toml")
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    parse_apps_data_from_file(args.filename)
