# builtin imports
from pathlib import Path
from typing import Any, Dict
from xml.etree.ElementTree import ElementTree, Element
from xml.etree import ElementTree as ET

class XMLDict:
    """
    Class to take an XML ElementTree from iMovieProj file and turn it into a dictionary-like format.
    """

    @staticmethod
    def LoadXMLDict(file:Path) -> Dict[str, Any]:
        xmltree : ElementTree = ElementTree()
        with open(file, "r") as xmlfile:
            xmltree = ET.parse(xmlfile)
        root = xmltree.getroot()
        if len(root) > 1:
            # file should have only one dict
            raise ValueError(f"Expected only one element (a dict) under iMovieProj XML root, found {len(root)}!")
        xmldict = root[0]
        if xmldict.tag != "dict":
            raise ValueError(f"Expected a dict under iMovieProj XML root, found {xmldict.tag}!")
        return XMLDict._parseDict(xmldict)

    @staticmethod
    def _parseDict(xmldict:Element):
        ret_val = {}

        if len(xmldict) % 2 != 0:
            raise ValueError(f"Expected the XML dictionary to have an even number of elements, found {len(xmldict)} elements!")
        for i in range(len(xmldict) // 2):
            if xmldict[2*i].tag != "key":
                raise ValueError(f"Expected the even keys under XML dict to be keys, found element {2*i} with tag {xmldict[2*i].tag}!")
            key = xmldict[2*i].text
            # print(f"In parseDict, about to parse value for key {key}")
            val = XMLDict._parse(xmldict[2*i + 1])
            ret_val[key] = val

        return ret_val

    @staticmethod
    def _parse(xmlvalue:Element):
        if xmlvalue.tag == "true":
            return True
        elif xmlvalue.tag == "false":
            return False
        elif xmlvalue.tag == "array":
            return [XMLDict._parse(elem) for elem in xmlvalue]
        else:
            if xmlvalue.text is None:
                if xmlvalue.tag == "string":
                    return str(xmlvalue.text)
                else:
                    raise ValueError(f"Expected XML Element with tag {xmlvalue.tag} to have a value, but found a value of None!")
            elif xmlvalue.tag == "string":
                return str(xmlvalue.text)
            elif xmlvalue.tag == "integer":
                return int(xmlvalue.text)
            elif xmlvalue.tag == "real":
                return float(xmlvalue.text)
            elif xmlvalue.tag == "dict":
                return XMLDict._parseDict(xmlvalue)
