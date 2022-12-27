# builtin imports
from typing import Any, Dict, Optional
from xml.etree.ElementTree import ElementTree, Element

class XMLDict:
    @staticmethod
    def XMLTreeToDict(xmltree:ElementTree):
        root = xmltree.getroot()
        if len(root) > 1:
            # file should have only one dict
            raise ValueError(f"Expected only one element (a dict) under iMovieProj XML root, found {len(root)}!")
        xmldict = root[0]
        if xmldict.tag != "dict":
            raise ValueError(f"Expected a dict under iMovieProj XML root, found {xmldict.tag}!")
        return XMLDict._parseDict(xmldict)

    @staticmethod
    def _parse(xmlvalue:Element):
        if xmlvalue.tag == "true":
            return True
        elif xmlvalue.tag == "false":
            return False
        else:
            if xmlvalue.text is None:
                raise ValueError(f"Expected XML Element with tag {xmlvalue.tag} to have a value, but found a value of None!")
            elif xmlvalue.tag == "string":
                return str(xmlvalue.text)
            elif xmlvalue.tag == "integer":
                return int(xmlvalue.text)
            elif xmlvalue.tag == "real":
                return float(xmlvalue.text)
            elif xmlvalue.tag == "array":
                return [XMLDict._parse(elem) for elem in xmlvalue]
            elif xmlvalue.tag == "dict":
                return XMLDict._parseDict(xmlvalue)

    @staticmethod
    def _parseDict(xmldict:Element):
        ret_val = {}

        if len(xmldict) % 2 != 0:
            raise ValueError(f"Expected the XML dictionary to have an even number of elements, found {len(xmldict)} elements!")
        for i in range(len(xmldict) // 2):
            if xmldict[2*i].tag != "key":
                raise ValueError(f"Expected the even keys under XML dict to be keys, found element {2*i} with tag {xmldict[2*i].tag}!")
            key = xmldict[2*i].text
            val = XMLDict._parse(xmldict[2*i + 1])
            ret_val[key] = val

        return ret_val

class VideoClip:
    """Tracking of video clip properties"""
    def __init__(self):
        self._duration = 0
        self._fileName = "empty"
        self._sceneName = "empty"
        self._inFrame = 0
        self._outFrame = 0
        self._partOfEdit = 0

    @property
    def Duration(self):
        """Method to check the clip's file name"""
        return self._duration
    @property
    def FileName(self):
        """Method to check the clip's file name"""
        return self._fileName
    @property
    def SceneName(self):
        """Method to check the clip's scene name"""
        return self._sceneName
    @property
    def InFrame(self):
        """Method to check the clip's file name"""
        return self._inFrame
    @property
    def OutFrame(self):
        """Method to check the clip's scene name"""
        return self._outFrame
    @property
    def InEdit(self):
        """Method to check if the current clip is part of the edit."""
        if self._partOfEdit == 0:
            return False
        elif self._partOfEdit == 1:
            return True
        else:
            return False

    def toString(self):
        return "scene " + self._sceneName + ", file " + self._fileName + ", in edit: " + str(self._partOfEdit)

class iMovieProj:
    """Class to handle structure of an iMovieHD project
    """

    def __init__(self, xmldict:Dict[str, Any]):
        nested_keys = ["audioClips", "audioTrashClips", "videoClips", "videoTrashClips"]
        self._other_elements = {key:xmldict[key] for key in xmldict.keys() if key not in nested_keys}
        self._audioClips      = self._getAudioClips(xmltree)
        self._audioTrashClips = self._getAudioTrashClips(xmltree)
        self._videoClips      = self._getVideoClips(xmltree)
        self._videoTrashClips = self._getVideoTrashClips(xmltree)

    @property
    def AudioClips(self):
        return self._audioClips
    @property
    def AudioTrashClips(self):
        return self._audioTrashClips
    @property
    def LastClipUniqueID(self) -> Optional[int]:
        return self._other_elements.get("lastClipUniqueID")
    @property
    def PlayheadPosition(self) -> Optional[int]:
        return self._other_elements.get("playheadPosition")
    @property
    def RelativePlayHeadPosition(self) -> Optional[float]:
        return self._other_elements.get("relativePlayHeadPosition")
    @property
    def SelectionEndFrame(self) -> Optional[int]:
        return self._other_elements.get("selectionEndFrame")
    @property
    def SelectionStartFrame(self) -> Optional[int]:
        return self._other_elements.get("selectionStartFrame")
    @property
    def SelectionType(self) -> Optional[int]:
        return self._other_elements.get("selectionType")
    @property
    def TimelineZoom(self) -> Optional[float]:
        return self._other_elements.get("timelineZoom")
    @property
    def Version(self) -> Optional[str]:
        return self._other_elements.get("version")
    @property
    def VideoClips(self):
        return self._videoClips
    @property
    def VideoStandard(self) -> Optional[str]:
        return self._other_elements.get("videoStandard")
    @property
    def VideoTrashClips(self):
        return self._videoTrashClips
    @property
    def WritingApplicationName(self) -> Optional[str]:
        return self._other_elements.get("writingApplicationName")
    @property
    def WritingApplicationVersion(self) -> Optional[str]:
        return self._other_elements.get("writingApplicationVersion")

    def _getAudioClips(xmltree)
    def _getAudioTrashClips(xmltree)
    def _getVideoClips(xmltree)
    def _getVideoTrashClips(xmltree)