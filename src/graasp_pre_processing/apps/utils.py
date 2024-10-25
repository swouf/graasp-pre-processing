import pandas as pd
from pandera import check_io
from .schemas import app_data_schema

@check_io(app_data_df=app_data_schema)
def split_by_item(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame) -> list[pd.DataFrame]:
    app_data_split = {name: item for name, item in app_data_df.groupby("itemId")}
    app_settings_split = {name: item for name, item in app_settings_df.groupby("itemId")}
    return app_data_split, app_settings_split
