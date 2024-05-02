import pandas as pd
from urllib.parse import urlparse

from graasp_pre_processing.apps import collaborative_ideation


def expand_app_data(app_data_raw: list, url) -> pd.DataFrame:
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        print(e)

    if app_id == "ff82329a-905a-4c59-85e0-3690113adc42":
        return collaborative_ideation.expand_app_data(app_data_raw)

    return pd.DataFrame(app_data_raw)


def expand_app_actions(app_actions_raw, url) -> pd.DataFrame:
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        print(e)

    if app_id == "ff82329a-905a-4c59-85e0-3690113adc42":
        return collaborative_ideation.expand_app_actions(app_actions_raw)

    return pd.DataFrame(app_actions_raw)


def expand_app_settings(app_settings_raw, url) -> pd.DataFrame:
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        print(e)

    if app_id == "ff82329a-905a-4c59-85e0-3690113adc42":
        return collaborative_ideation.expand_app_settings(app_settings_raw)

    return pd.DataFrame(app_settings_raw)
