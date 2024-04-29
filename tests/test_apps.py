from graasp_pre_processing.apps.apps import parse_apps_data
import pandas as pd
import pytest
from pathlib import Path


@pytest.fixture
def apps_data_file():
    current_path = Path(__file__).parent
    
    return [open(Path(current_path / "fixtures/apps_data.json"), "r+t")]


class TestApps:
    def test_parse_apps_data(self, apps_data_file):
        app_data, app_actions, app_settings, items = parse_apps_data(*apps_data_file)
        assert isinstance(app_data, pd.DataFrame)
        assert isinstance(app_actions, pd.DataFrame)
        assert isinstance(app_settings, pd.DataFrame)
        assert isinstance(items, pd.DataFrame)
