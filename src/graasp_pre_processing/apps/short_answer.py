import logging
import pandas as pd

log = logging.getLogger(__name__)

def expand_data_field(row):
    d = row.to_dict()
    data_field = d.pop("data")
    log.info("Data field: ", data_field)
    return pd.Series(d | data_field)


def expand_app_data(app_data_raw: list) -> pd.DataFrame:
    data = pd.DataFrame(app_data_raw)
    data = data.apply(expand_data_field, axis="columns")
    return data


def expand_app_actions(app_actions_raw) -> pd.DataFrame:
    data = pd.DataFrame(app_actions_raw)
    data = data.apply(expand_data_field, axis="columns")
    return data


def expand_app_settings(app_settings_raw) -> pd.DataFrame:
    data = pd.DataFrame(app_settings_raw)
    data = data.apply(expand_data_field, axis="columns")
    return data
