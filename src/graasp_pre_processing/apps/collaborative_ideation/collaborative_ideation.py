import pandas as pd

import logging
from pandera import check_io

from graasp_pre_processing.apps.utils import split_by_item

from ..schemas import app_data_schema, app_settings_schema
from .schemas import responses_schema

log = logging.getLogger(__name__)

url_collaborative_ideation = "https://apps.graasp.org/ff82329a-905a-4c59-85e0-3690113adc42/latest/index.html"
collaborative_ideation_app_name = 'collaborative-ideation'

def expand_data_field(row):
    d = row.to_dict()
    data_field = d.pop("data")
    return pd.Series(d | data_field)

def get_app_type_from_url(url: str) -> str:
    if url == url_collaborative_ideation:
        return collaborative_ideation_app_name
    else:
        return pd.NA

def get_number_of_assistants(app_settings_df: pd.DataFrame) -> int:
    try:
        n = len(app_settings_df.set_index('name').loc['assistants']['data']['assistants'])
        log.debug("Number of assistants: %s", n)
        return n
    except Exception as e:
        log.info("No assistants found.")
        return pd.NA
    
def get_visibility_mode(app_settings_df: pd.DataFrame) -> str:
    try:
        m = app_settings_df.set_index('name').loc['activity']['data']['mode']
        log.debug("Visibility mode: %s", m)
        return m
    except Exception as e:
        log.info("Visibility mode undefined.")
        return pd.NA
    
def get_last_response(row) -> dict:
    r = row['response']
    response = None
    responses_chain = pd.NA
    if isinstance(r, list):
        response = r[0]
        responses_chain = r
    else:
        response = r
    return pd.Series({"response": response, "responsesChain": responses_chain})
    
def process_single_app(app_data_df, app_settings_df, apps):
    itemIds = app_data_df['itemId'].unique()
    if len(itemIds) > 1:
        raise Exception("The itemId is not unique.")
    else:
        itemId = itemIds[0]
        app = apps.loc[itemId]
        if app['app'] != collaborative_ideation_app_name:
            return None
        responses = app_data_df.where(app_data_df['type'] == 'response').dropna(how='all')
        responses = responses.apply(expand_data_field, axis="columns")
        log.debug(responses.columns)
        responses = responses.drop('response', axis="columns")\
            .join(responses.apply(get_last_response, result_type="expand", axis="columns"))
        log.debug(responses.columns)
        if 'bot' in responses.columns:
            responses['bot'] = responses['bot'].fillna(False)
        else:
            responses['bot'] = False
        responses['numberOfAssistants'] = get_number_of_assistants(app_settings_df)
        responses['visibilityMode'] = get_visibility_mode(app_settings_df)
        return responses

@check_io(out=responses_schema, app_data_df=app_data_schema, app_settings_df=app_settings_schema)
def get_df_responses(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, items_df):
    apps = items_df.where(items_df['type'] == 'app').dropna(how='all')
    apps['url'] = apps['extra'].apply(lambda x: x['app']['url'])
    apps['app'] = apps['url'].apply(get_app_type_from_url)

    data_split, settings_split = split_by_item(app_data_df, app_settings_df)
    collab_app_split_df = [process_single_app(data_split[key], settings_split[key], apps) for key in data_split.keys()]

    return pd.concat(collab_app_split_df, axis="index")