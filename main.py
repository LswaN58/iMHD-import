# builtin imports
from pathlib import Path
from typing import Any, Dict
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element
# 3rd-party imports
import bpy
# local imports
from importer import iMovieProj, XMLDict

X_RESOLUTION = 640
Y_RESOLUTION = 480
BASE_FILEPATH = Path("/Volumes/Little_Black_Box/LBB Users/LBB lukeswanson/LBB Movies")

path_of_proj_file = BASE_FILEPATH / Path("Outdoor_Movie/outdoor_movie_edit.iMovieProj")
path_of_clips = BASE_FILEPATH / Path("Outdoor_Movie/")

xmltree : ElementTree    = ET.parse(path_of_proj_file)
xmldict : Dict[str, Any] = XMLDict.XMLTreeToDict(xmltree)
project : iMovieProj     = iMovieProj(xmldict=xmldict)