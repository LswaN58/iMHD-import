# builtin imports
from pathlib import Path
from typing import Any, Dict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree
# 3rd-party imports
# local imports
from importer import iMovieProj, XMLDict
from config import PROJ_PATH

xmltree : ElementTree    = ET.parse(PROJ_PATH)
xmldict : Dict[str, Any] = XMLDict.XMLTreeToDict(xmltree)
project : iMovieProj     = iMovieProj(xmldict=xmldict)