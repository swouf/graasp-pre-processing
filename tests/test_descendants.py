import logging
from pathlib import Path
import sys
import pytest

from graasp_pre_processing.descendants import parse_descendants

logging.basicConfig(stream=sys.stdout, level=logging.debug)
log = logging.getLogger(__name__)

@pytest.fixture
def descendants_file():
    current_path = Path(__file__).parent

    return [open(Path(current_path / "fixtures/descendants.json"), "r+t")]


class TestMembers:
    def test_parse_descendants(self, descendants_file):
        descendants = parse_descendants(*descendants_file)
        log.info(descendants)
        columns = descendants.columns.values
        assert "id" == descendants.index.name
        assert "name" in columns
        assert "parentId" in columns
