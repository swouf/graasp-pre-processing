import numpy as np
import pandas as pd

import logging
from pandera import check_io, check_output

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
    
def get_instructions(app_settings_df: pd.DataFrame) -> str:
    try:
        instructions = app_settings_df.set_index('name').loc['instructions']['data']['title']['content']
        return instructions
    except Exception as e:
        log.info("No instructions found.")
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
        response = r[-1]
        responses_chain = r
    else:
        response = r
    return pd.Series({"response": response, "responsesChain": responses_chain})

def get_votes(app_data_df: pd.DataFrame) -> pd.Series:
    votes = app_data_df.where(app_data_df['type'] == 'Vote')\
        .dropna(how='all')\
        .apply(expand_data_field, axis="columns")\
        .reset_index()
    if votes.empty:
        return None
    votes = pd.Series(votes.get(['id', 'responseRef']).groupby('responseRef')\
        .count()['id']\
        .rename('numberOfVotes'), dtype=pd.Int64Dtype)
    log.debug(votes)
    return votes


@check_io(out=responses_schema, lazy=True)
def process_single_app(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, apps) -> pd.DataFrame:
    itemIds = app_data_df['itemId'].unique()
    if len(itemIds) > 1:
        raise Exception("The itemId is not unique.")
    else:
        itemId = itemIds[0]
        app = apps.loc[itemId]
        if pd.isna(app['app']):
            return None
        if app['app'] != collaborative_ideation_app_name:
            return None
        log.debug("Processing single app...")
        responses = app_data_df.where(app_data_df['type'] == 'response').dropna(how='all')
        responses = responses.apply(expand_data_field, axis="columns")
        if 'response' not in responses.columns.values:
            return None
        log.debug(responses.columns.values)

        responses = responses.drop('response', axis="columns")\
            .join(responses.apply(get_last_response, result_type="expand", axis="columns"))
        log.debug(responses.columns)

        votes = get_votes(app_data_df)
        if votes is not None:
            responses = responses.join(votes)
            responses['numberOfVotes'] = responses['numberOfVotes'].fillna(0)
            log.debug("Responses with votes:")
            log.debug(responses['numberOfVotes'])
        if 'bot' in responses.columns:
            responses['bot'] = responses['bot'].fillna(False)
        else:
            responses['bot'] = False
        responses['numberOfAssistants'] = get_number_of_assistants(app_settings_df)
        responses['visibilityMode'] = get_visibility_mode(app_settings_df)
        responses['instructions'] = get_instructions(app_settings_df)
        return responses

# @check_io(app_data_df=app_data_schema, app_settings_df=app_settings_schema)
@check_io(out=responses_schema, app_data_df=app_data_schema, app_settings_df=app_settings_schema, lazy=True)
def get_df_responses(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, items_df, item_ids_to_filter: list[str]=None):
    apps = items_df.where(items_df['type'] == 'app').dropna(how='all')
    apps['url'] = apps['extra'].apply(lambda x: x['app']['url'])
    apps['app'] = apps['url'].apply(get_app_type_from_url)

    data_split, settings_split = split_by_item(app_data_df, app_settings_df)
    collab_app_split_df = [process_single_app(data_split[key], settings_split[key], apps) for key in data_split.keys()]
    
    all_responses = pd.concat(collab_app_split_df, axis="index").sort_index(axis="columns")
    
    if item_ids_to_filter is not None:
        all_responses = all_responses[all_responses['itemId'].isin(item_ids_to_filter) == False]  # noqa: E712

    return all_responses