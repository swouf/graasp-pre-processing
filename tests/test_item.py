from datetime import datetime
from pathlib import Path
import pytest

from graasp_pre_processing.entities.Item import Item


@pytest.fixture
def item_file():
    current_path = Path(__file__).parent

    return open(Path(current_path / "fixtures/item.json"), "r+t")


class TestItem:
    def test_new_item(self, item_file):
       item = Item(item_file)
       assert isinstance(item.id, str)
       assert isinstance(item.creatorId, str)
       assert isinstance(item.createdAt, datetime)