import logging
import pandas as pd
from urllib.parse import urlparse

from graasp_pre_processing.apps import collaborative_ideation, likert_scale

log = logging.getLogger(__name__)


def expand_app_data(app_data_raw: list, url) -> pd.DataFrame:
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        log.warning(e)

    if app_id == "ff82329a-905a-4c59-85e0-3690113adc42":
        return collaborative_ideation.expand_app_data(app_data_raw)
    if app_id == "fef4a130-0fbc-47f4-bc41-48e3ba0c41b4":
        return likert_scale.expand_app_data(app_data_raw)

    return pd.DataFrame(app_data_raw)


def expand_app_actions(app_actions_raw, url) -> pd.DataFrame:
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        log.warning(e)

    if app_id == "ff82329a-905a-4c59-85e0-3690113adc42":
        return collaborative_ideation.expand_app_actions(app_actions_raw)
    if app_id == "fef4a130-0fbc-47f4-bc41-48e3ba0c41b4":
        return likert_scale.expand_app_actions(app_actions_raw)

    return pd.DataFrame(app_actions_raw)


def match_exp_settings(app_settings_raw: list, app_id: str) -> pd.DataFrame:
    match app_id:
        case "ff82329a-905a-4c59-85e0-3690113adc42":
            return collaborative_ideation.expand_app_settings(app_settings_raw)
        case "fef4a130-0fbc-47f4-bc41-48e3ba0c41b4":
            return likert_scale.expand_app_settings(app_settings_raw)
        case _:
            pd.DataFrame(app_settings_raw)


def expand_app_settings(app_settings_raw: list, url: str) -> pd.DataFrame | None:
    if len(app_settings_raw) == 0:
        return None
    url_parsed = urlparse(url)
    path = url_parsed.path
    app_id = ""
    try:
        app_id = path.split("/")[1]
    except IndexError as e:
        log.warning(e)

    app_settings = match_exp_settings(app_settings_raw, app_id).set_index("id")

    log.info(app_settings.index.names)

    return app_settings
