from graasp_pre_processing.apps.apps import parse_apps_data, parse_data
import pandas as pd
import pytest
from pathlib import Path
import sys

import logging

logging.basicConfig(stream=sys.stdout, level=logging.debug)
log = logging.getLogger(__name__)


@pytest.fixture
def apps_data_file():
    current_path = Path(__file__).parent

    return [open(Path(current_path / "fixtures/apps_data.json"), "r+t")]
    # return [open(Path(current_path / "fixtures/apps_data_2.json"), "r+t")]


@pytest.fixture
def item():
    return {
        "id": "aabbccdd",
        "name": "Idéation",
        "displayName": "Idéation",
        "description": "",
        "type": "app",
        "createdAt": "2024-04-22T20:01:20.677Z",
        "updatedAt": "2024-04-22T20:01:20.677Z",
        "deletedAt": None,
        "extra": {
            "url": "https://apps.graasp.org/ff82329a-905a-4c59-85e0-3690113adc42/latest/index.html",
            "settings": {},
        },
        "settings": pd.NA,
        "path": "bbccddee.aabbccdd",
        "lang": "fr",
    }


@pytest.fixture
def app_data_raw(item):
    return [
        [
            {
                "id": "1",
                "type": "response",
                "visibility": "item",
                "createdAt": "2024-04-23T15:36:19.948Z",
                "updatedAt": "2024-04-23T15:36:19.948Z",
                "member": {
                    "id": "123456789",
                    "name": "Tester Testarolli",
                    "email": "test@test.org",
                    "extra": {"lang": "en"},
                },
                "creator": {
                    "id": "123456789",
                    "name": "Tester Testarolli",
                    "email": "test@test.org",
                    "extra": {"lang": "en"},
                },
                "item": item,
                "data": {
                    "round": 0.0,
                    "originalResponse": "Hello!",
                    "response": "Hello not!",
                    "assistantId": pd.NA,
                    "bot": pd.NA,
                    "parentId": pd.NA,
                },
            },
            {
                "id": "2",
                "type": "response",
                "visibility": "item",
                "createdAt": "2024-04-23T15:36:19.948Z",
                "updatedAt": "2024-04-23T15:36:19.948Z",
                "member": {
                    "id": "123456789",
                    "name": "Tester Testarolli",
                    "email": "test@test.org",
                    "extra": {"lang": "en"},
                },
                "creator": {
                    "id": "123456789",
                    "name": "Tester Testarolli",
                    "email": "test@test.org",
                    "extra": {"lang": "en"},
                },
                "item": item,
                "data": {
                    "round": 0.0,
                    "originalResponse": "Hello 2!",
                    "response": "Hello not!",
                    "assistantId": pd.NA,
                    "bot": pd.NA,
                    "parentId": pd.NA,
                },
            },
        ]
    ]


class TestApps:
    def test_parse_apps_data(self, apps_data_file):
        app_data, app_actions, app_settings, items = parse_apps_data(*apps_data_file)
        assert isinstance(app_data, pd.DataFrame)
        assert isinstance(app_actions, pd.DataFrame)
        assert isinstance(app_settings, pd.DataFrame)
        assert isinstance(items, pd.DataFrame)

        log.debug(items.sample(5).head(5))

        assert app_settings.index.name == "id"
        assert items.index.name == "id"
        assert items.index.is_unique

    def test_parse_data(self, app_data_raw, item):
        parsed = parse_data(*app_data_raw, item)
        print(parsed.columns.values)
        assert "creatorId" in parsed.columns.values
