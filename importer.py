# builtin imports
from typing import Any, Dict, List, Optional
from xml.etree.ElementTree import ElementTree, Element
# local imports
from AudioClip import AudioClip
from VideoClip import VideoClip, VideoClipFactory

class XMLDict:
    """
    Class to take an XML ElementTree from iMovieProj file and turn it into a dictionary-like format.
    """

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
        elif xmlvalue.tag == "array":
            return [XMLDict._parse(elem) for elem in xmlvalue]
        else:
            if xmlvalue.text is None:
                raise ValueError(f"Expected XML Element with tag {xmlvalue.tag} to have a value, but found a value of None!")
            elif xmlvalue.tag == "string":
                return str(xmlvalue.text)
            elif xmlvalue.tag == "integer":
                return int(xmlvalue.text)
            elif xmlvalue.tag == "real":
                return float(xmlvalue.text)
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
            print(f"In parseDict, about to parse value for key {key}")
            val = XMLDict._parse(xmldict[2*i + 1])
            ret_val[key] = val

        return ret_val

class iMovieProj:
    """Class to handle structure of an iMovieHD project
    """

    def __init__(self, xmldict:Dict[str, Any]):
        nested_keys = ["audioClips", "audioTrashClips", "videoClips", "videoTrashClips"]
        self._other_elements  : Dict[str, Any]  = {key:xmldict[key] for key in xmldict.keys() if key not in nested_keys}
        self._audioClips      : List[AudioClip] = [AudioClip(aclip) for aclip in xmldict.get("audioClips", [])]
        self._audioTrashClips : List[AudioClip] = [AudioClip(aclip) for aclip in xmldict.get("audioTrashClips", [])]
        self._videoClips      : List[VideoClip] = [VideoClipFactory.FromDict(vclip) for vclip in xmldict.get("videoClips", [])]
        self._videoTrashClips : List[VideoClip] = [VideoClipFactory.FromDict(vclip) for vclip in xmldict.get("videoClips", [])]

    def __repr__(self) -> str:
        return f"iMovieProj object: {len(self.VideoClips)} video clips; {len(self.AudioClips)} audio clips; {self.VideoStandard} format"

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
