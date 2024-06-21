from datetime import datetime
from io import TextIOWrapper
import json


def get_deleted_at(d):
    if d is not None:
        return datetime.fromisoformat(d)
    else:
        return None

class Item:
    def __init__(self, filehandler: TextIOWrapper, codingTable = None):
        data = json.load(filehandler)
        self.id = data['id']
        self.name = data['name']
        self.displayName = data['displayName']
        self.description = data['description']
        self.type = data['type']
        ca = data['createdAt']
        print(ca)
        self.createdAt = datetime.fromisoformat(ca)
        self.updatedAt = datetime.fromisoformat(data['updatedAt'])
        self.deletedAt = get_deleted_at(data['deletedAt'])
        self.settings = data['settings']
        self.creatorId = data['creator']['id']