import logging
import pandas as pd
from pandera import check_input, check_io

from graasp_pre_processing.apps.utils import split_by_item

from ..schemas import app_data_schema, app_settings_schema

log = logging.getLogger(__name__)

url_multiple_choice = "https://apps.graasp.org/b5428aa6-00cf-4382-ac6e-0b0c4367b9a2/latest/index.html"
url_likert_scale = "https://apps.graasp.org/fef4a130-0fbc-47f4-bc41-48e3ba0c41b4/latest/index.html"
url_short_answer = "https://apps.graasp.org/75438e6e-8442-4ffe-9a16-d1bebf5f8952/latest/index.html"

survey_apps_urls = {
    url_multiple_choice: "multiple-choice",
    url_likert_scale: "likert-scale",
    url_short_answer: "short-answer",
}

def get_app_type_from_url(url: str) -> str:
    try:
        return survey_apps_urls[url]
    except KeyError as e:
        log.debug(e)
        return pd.NA

@check_io(app_data_df=app_data_schema, app_settings_df=app_settings_schema)
def process_multiple_choice_app_data(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, itemId: str):
    d = app_data_df.where(app_data_df['type'] == 'user-answer').dropna(how='all')
    d = d.sort_values("updatedAt").groupby("creatorId").last()
    return d['data'].apply(lambda x: x['multipleKey']).rename(itemId)

@check_io(app_data_df=app_data_schema, app_settings_df=app_settings_schema)
def process_likert_scale_app_data(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, itemId: str, force_columns_item_id=False):
    d = app_data_df.where(app_data_df['type'] == 'user-answer').dropna(how='all')
    d = d.sort_values("updatedAt").groupby("creatorId").last()
    try:
        likertItem = app_settings_df.set_index('name').loc['likertItem']['data']['item']
        label = likertItem['key']
    except Exception as e:
        log.warning(e)
    if len(label) == 0 or force_columns_item_id:
        label = itemId
    return d['data'].apply(lambda x: x['answer']).rename(label)

@check_io(app_data_df=app_data_schema, app_settings_df=app_settings_schema)
def process_short_answer_app_data(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, itemId: str):
    d = app_data_df.where(app_data_df['type'] == 'user-answer').dropna(how='all')
    d = d.sort_values("updatedAt").groupby("creatorId").last()
    return d['data'].apply(lambda x: x['answer']).rename(itemId)
    
def process_single_survey_app_data(app_data_df, app_settings_df, apps, force_columns_item_id=False):
    itemIds = app_data_df['itemId'].unique()
    if len(itemIds) > 1:
        raise Exception("The itemId is not unique.")
    else:
        itemId = itemIds[0]
        app = apps.loc[itemId]

        match app['app']:
            case 'multiple-choice':
                return process_multiple_choice_app_data(app_data_df, app_settings_df, itemId)
            case 'likert-scale':
                return process_likert_scale_app_data(app_data_df, app_settings_df, itemId, force_columns_item_id)
            case 'short-answer':
                return process_short_answer_app_data(app_data_df, app_settings_df, itemId)
            case _:
                log.warning("No app recognized for item %s", itemId)
                return None

@check_input(app_data_schema)
def get_df_answer(app_data_df: pd.DataFrame, app_settings_df: pd.DataFrame, items_df, force_columns_item_id=False):
    apps = items_df.where(items_df['type'] == 'app').dropna(how='all')
    apps['url'] = apps['extra'].apply(lambda x: x['app']['url'])
    apps['app'] = apps['url'].apply(get_app_type_from_url).fillna('no-app')

    data_split, settings_split = split_by_item(app_data_df, app_settings_df)

    survey_split_df = []
    for key in data_split.keys():
        
        ad = data_split[key]
        try:
            s = settings_split[key]
        except KeyError as e:
            log.warning("No such thing as %s", key, exc_info=True)
            s = None

        part = process_single_survey_app_data(ad, s, apps, force_columns_item_id)
        survey_split_df.append(part)

    return pd.concat(survey_split_df, axis="columns")