import argparse
from io import TextIOWrapper
import json
import pandas as pd
from pathlib import Path
import logging

from .schemas import app_data_schema, app_settings_schema

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


def transform_destructure_to_id(data: pd.DataFrame, account=True):
    creatorId = None
    accountId = None
    itemId = None
    d = data
    try:
        creatorId = data["creator"].apply(lambda x: x["id"]).rename("creatorId")
        d = d.join(creatorId).drop('creator', axis="columns")
        if account:
            accountId = data["account"].apply(lambda x: x["id"]).rename("accountId")
            d = d.join(accountId).drop('account', axis="columns")
        itemId = data["item"].apply(lambda x: x["id"]).rename("itemId")
        d = d.join(itemId).drop('item', axis="columns")
    except KeyError as e:
        log.warning(e)
    return d


def parse_actions(actions_raw):
    actions = pd.DataFrame(actions_raw)
    return actions


def parse_data(app_data_raw: list) -> pd.DataFrame:
    app_data_df = pd.DataFrame(app_data_raw)
    app_data_df = transform_destructure_to_id(app_data_df)
    app_data_df = app_data_df.set_index('id')
    app_data_df = app_data_schema.validate(app_data_df)
    return app_data_df


def parse_settings(settings_raw: list) -> pd.DataFrame:
    app_settings = pd.DataFrame(settings_raw)
    app_settings = transform_destructure_to_id(app_settings, account=False)
    app_settings = app_settings.set_index("id")
    app_settings = app_settings_schema.validate(app_settings)
    return app_settings

def parse_apps_data(
    filehandler: TextIOWrapper,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Parse multiple apps data from an already opened file.
    """
    data = json.load(filehandler)
    app_data_df = parse_data(data['appData'])
    app_actions_df = parse_actions(data['appActions'])
    app_settings_df = parse_settings(data['appSettings'])
    return app_data_df, app_actions_df, app_settings_df


def parse_apps_data_from_file(
    path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Return datasets for app_data, actions, and settings.
    """
    fullPath = Path(path).expanduser().absolute()
    with open(fullPath, "+r") as openedFile:
        return parse_apps_data(openedFile)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()

    parse_apps_data_from_file(args.filename)
