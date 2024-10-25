import logging
from pathlib import Path
from re import Match, compile
from string import Template

import pandas as pd

from graasp_pre_processing.apps.apps import parse_apps_data_from_file
from graasp_pre_processing.descendants import parse_descendants_from_file
from graasp_pre_processing.entities.Item import Item
from graasp_pre_processing.errors.FilesErrors import DirError
from graasp_pre_processing.members import parse_members_from_file

log = logging.getLogger(__name__)

patternTemplate = Template("^$prefix\_\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,}Z\.json$$")
patternItem = compile(patternTemplate.substitute({"prefix": "item"}))
patternApps = compile(patternTemplate.substitute({"prefix": "apps"}))
patternDescendants = compile(patternTemplate.substitute({"prefix": "descendants"}))
patternMembers = compile(patternTemplate.substitute({"prefix": "members"}))

def load_data_from_dir(dir: Path) -> tuple[Item, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rootItem: Item = None
    if not dir.is_dir():
        raise DirError(dir)
    
    itemPath: Path
    appsPath: Path
    descendantsPath: Path
    membersPath: Path
    
    for child in dir.iterdir():
         itemMatch: Match = patternItem.fullmatch(child.name)
         appsMatch: Match = patternApps.fullmatch(child.name)
         descendantsMatch: Match = patternDescendants.fullmatch(child.name)
         membersMatch: Match = patternMembers.fullmatch(child.name)
         if itemMatch is not None:
             itemPath = child.absolute()
         elif appsMatch is not None:
             appsPath = child.absolute()
         elif descendantsMatch is not None:
             descendantsPath = child.absolute()
         elif membersMatch is not None:
             membersPath = child.absolute()
    
    with open(itemPath, 'r+t') as itemFile:
        rootItem = Item(filehandler=itemFile)

    items_df = parse_descendants_from_file(descendantsPath)
    app_data_df, app_actions_df, app_settings_df = parse_apps_data_from_file(appsPath)
    members_df = parse_members_from_file(membersPath)


    return (rootItem, items_df, members_df, app_data_df, app_actions_df, app_settings_df)