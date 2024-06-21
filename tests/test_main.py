from datetime import datetime
from pathlib import Path
import pytest
from graasp_pre_processing.main import load_data_from_dir


@pytest.fixture
def data_dir_path():
    current_path = Path(__file__).parent

    return Path(current_path / "fixtures/data_dir")


class TestMain:
    def test_load_data(self, data_dir_path):
        (item, descendants) = load_data_from_dir(data_dir_path)
        assert isinstance(item.id, str)
        assert isinstance(item.creatorId, str)
        assert isinstance(item.createdAt, datetime)
        columns = descendants.columns.values
        assert "id" == descendants.index.name
        assert "name" in columns
        assert "parentId" in columns