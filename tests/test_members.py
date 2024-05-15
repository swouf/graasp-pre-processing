from pathlib import Path
import pytest

from graasp_pre_processing.members import parse_members


@pytest.fixture
def members_file():
    current_path = Path(__file__).parent

    return [open(Path(current_path / "fixtures/members.json"), "r+t")]


class TestMembers:
    def test_parse_members(self, members_file):
        members = parse_members(*members_file)
        print(members)
        assert len(members) == 3
        assert "id" in members.columns.values
        assert "name" in members.columns.values
        assert "email" in members.columns.values
