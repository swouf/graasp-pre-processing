import logging
from pathlib import Path
from re import Match, compile
from string import Template

from graasp_pre_processing.descendants import parse_descendants_from_file
from graasp_pre_processing.entities.Item import Item
from graasp_pre_processing.errors.FilesErrors import DirError

log = logging.getLogger(__name__)

patternTemplate = Template("^$prefix\_\d{4}\-\d{2}\-\d{2}T\d{2}:\d{2}:\d{2}\.\d{1,}Z\.json$$")
patternItem = compile(patternTemplate.substitute({"prefix": "item"}))
patternApps = compile(patternTemplate.substitute({"prefix": "apps"}))
patternDescendants = compile(patternTemplate.substitute({"prefix": "descendants"}))

def load_data_from_dir(dir: Path):
    rootItem: Item = None
    if not dir.is_dir():
        raise DirError(dir)
    
    itemPath: Path
    appsPath: Path
    descendantsPath: Path
    
    for child in dir.iterdir():
         itemMatch: Match = patternItem.fullmatch(child.name)
         appsMatch: Match = patternApps.fullmatch(child.name)
         descendantsMatch: Match = patternDescendants.fullmatch(child.name)
         if itemMatch is not None:
             itemPath = child.absolute()
         elif appsMatch is not None:
             appsPath = child.absolute()
         elif descendantsMatch is not None:
             descendantsPath = child.absolute()
    
    with open(itemPath, 'r+t') as itemFile:
        rootItem = Item(itemFile)

    descendants = parse_descendants_from_file(descendantsPath)


    return (rootItem, descendants)