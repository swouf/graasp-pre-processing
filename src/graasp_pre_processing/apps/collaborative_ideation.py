import pandas as pd


def expand_data_field(row):
    d = row.to_dict()
    data_field = d.pop("data")
    return pd.Series(d | data_field)


def expand_app_data(app_data_raw):
    data = pd.DataFrame(app_data_raw)
    data = data.apply(expand_data_field, axis="columns")
    return data


def expand_app_actions(app_actions_raw):
    data = pd.DataFrame(app_actions_raw)
    data = data.apply(expand_data_field, axis="columns")
    return data
