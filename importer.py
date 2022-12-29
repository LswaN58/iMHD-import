# builtin imports
from typing import Any, Dict, List, Optional
from xml.etree.ElementTree import ElementTree, Element

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

class AudioPushPin:
    """Tracking of push-pin properties within a clip"""
    def __init__(self, pin_dict:Dict[str, Any]):
        required = {"audioFrame", "originalClipFrame", "videoFrame"}
        if not set(pin_dict.keys()).issuperset(required):
            raise ValueError(f"AudioPushPin is missing required elements {required.difference(set(pin_dict.keys()))}!")
        self._audio_frame       = pin_dict['audioFrame']
        self._originalClipFrame = pin_dict['originalClipFrame']
        self._videoFrame        = pin_dict['videoFrame']
        self._other_elements    = {pin:pin_dict[pin] for pin in pin_dict.keys() if pin not in required}

    @property
    def AudioFrame(self) -> int:
        return self._audio_frame
    @property
    def ClipUID(self) -> Optional[int]:
        return self._other_elements.get('clipUID')
    @property
    def OriginalClipFrame(self) -> int:
        return self._originalClipFrame
    @property
    def OriginalClipUID(self) -> Optional[int]:
        return self._other_elements.get('originalClipUID')
    @property
    def VideoFrame(self) -> int:
        return self._videoFrame

class AudioClip:
    """Tracking of audio clip properties"""
    def __init__(self, clip_dict:Dict[str, Any]):
        if not clip_dict.get('class') == "audio":
            raise ValueError(f"AudioClip constructor was given a dict of class {clip_dict.get('class')}!")
        required = {"duration","file","name","in","out","startFrame","track","trimmedEndFrame","trimmedStartFrame"}
        if not set(clip_dict.keys()).issuperset(required):
            raise ValueError(f"AudioClip is missing required elements {required.difference(set(clip_dict.keys()))}!")
        self._duration     = clip_dict['duration']
        self._fileName     = clip_dict['file']
        self._name         = clip_dict['name']
        self._inFrame      = clip_dict['in']
        self._outFrame     = clip_dict['out']
        self._startFrame   = clip_dict['startFrame']
        self._track        = clip_dict['track']
        self._trimmedStart = clip_dict['trimmedStartFrame']
        self._trimmedEnd   = clip_dict['trimmedEndFrame']

        self._filtered_list  = [AudioClip(clip) for clip in clip_dict.get('imaeFilteredList', [])]
        self._push_pins      = [AudioPushPin(pin) for pin in clip_dict.get('pushPins', [])]
        self._other_elements = {clip:clip_dict[clip] for clip in clip_dict.keys() if clip not in required}

    @property
    def Duration(self) -> int:
        return self._duration
    @property
    def FileName(self) -> str:
        return self._fileName
    @property
    def InFrame(self) -> int:
        return self._inFrame
    @property
    def OutFrame(self) -> int:
        return self._outFrame
    @property
    def Image4CC(self) -> Optional[int]:
        return self._other_elements.get('imae4cc')
    @property
    def imagefilteredlist(self) -> list:
        return self._filtered_list
    @property
    def ImageVersion(self) -> Optional[int]:
        return self._other_elements.get('imaeVersion')
    @property
    def IsSelected(self) -> Optional[bool]:
        return self._other_elements.get('isSelected')
    @property
    def Name(self) -> str:
        return self._name
    @property
    def PushPins(self) -> List[AudioPushPin]:
        return self._push_pins
    @property
    def StartFrame(self) -> int:
        return self._startFrame
    @property
    def TimeScale(self) -> Optional[int]:
        return self._other_elements.get('timeScale')
    @property
    def Track(self) -> int:
        return self._track
    @property
    def TrimmedEndFrame(self) -> int:
        return self._trimmedEnd
    @property
    def TrimmedStartFrame(self) -> int:
        return self._trimmedStart
    @property
    def UniqueID(self) -> Optional[bool]:
        return self._other_elements.get('uniqueID')
    @property
    def Version(self) -> Optional[str]:
        return self._other_elements.get('version')

class VideoClip:
    """Tracking of video clip properties"""
    # TODO: IsFiltered should figure out if we got a clip that had filter applied,
    # and based on IsFiltered, we should retrieve original clip, not rendered filter clip.
    def __init__(self, clip_dict):
        if not clip_dict.get('class') == "video":
            raise ValueError(f"VideoClip constructor was given a dict of class {clip_dict.get('class')}!")
        required = {"duration","file","name","in","out","track"}
        if not set(clip_dict.keys()).issuperset(required):
            raise ValueError(f"VideoClip is missing required elements {required.difference(set(clip_dict.keys()))}!")
        self._duration     = clip_dict['duration']
        self._fileName     = clip_dict['file']
        self._name         = clip_dict['name']
        self._inFrame      = clip_dict['in']
        self._outFrame     = clip_dict['out']
        self._track        = clip_dict['track']

        self._other_elements = {clip:clip_dict[clip] for clip in clip_dict.keys() if clip not in required}

    @property
    def Duration(self) -> int:
        return self._duration
    @property
    def FileName(self) -> str:
        return self._fileName
    @property
    def InFrame(self) -> int:
        return self._inFrame
    @property
    def OutFrame(self) -> int:
        return self._outFrame
    @property
    def IsSelected(self) -> Optional[bool]:
        return self._other_elements.get('isSelected')
    @property
    def MediaHandlePost(self) -> Optional[bool]:
        return self._other_elements.get('mediaHandlePost')
    @property
    def Name(self) -> str:
        return self._name
    @property
    def ShelfX(self) -> Optional[int]:
        return self._other_elements.get('shelfX')
    @property
    def ShelfY(self) -> Optional[int]:
        return self._other_elements.get('shelfY')
    @property
    def Thumb(self) -> Optional[int]:
        return self._other_elements.get('thumb')
    @property
    def TimeScale(self) -> Optional[int]:
        return self._other_elements.get('timeScale')
    @property
    def Track(self) -> int:
        return self._track
    @property
    def Type(self) -> Optional[int]:
        return self._other_elements.get('type')
    @property
    def UniqueID(self) -> Optional[bool]:
        return self._other_elements.get('uniqueID')
    @property
    def Version(self) -> Optional[str]:
        return self._other_elements.get('version')

    @property
    def InEdit(self):
        """Method to check if the current clip is part of the edit."""
        if self._track == 0:
            return False
        elif self._track == 1:
            return True
        else:
            return False

    def toString(self):
        return "scene " + self._name + ", file " + self._fileName + ", in edit: " + str(self.InEdit)

class Transition(VideoClip):
    """Subclass of VideoClip to handle info about Transitions"""
    def __init__(self, clip_dict):
        required = {"duration","file","name","in","out","startFrame","track","framesTakenAfter","framesTakenBefore"}
        if not set(clip_dict.keys()).issuperset(required):
            raise ValueError(f"VideoClip is missing required elements {required.difference(set(clip_dict.keys()))}!")
        super().__init__(clip_dict)
        self._framesBefore = clip_dict['framesTakenBefore']
        self._framesAfter  = clip_dict['framesTakenAfter']
        self._startFrame   = clip_dict['startFrame']

        self._replaced_clips = [VideoClip(clip) for clip in clip_dict.get('replacedClips', [])]

    @property
    def FramesTakenAfter(self) -> int:
        return self._framesAfter
    @property
    def FramesTakenBefore(self) -> int:
        return self._framesBefore
    @property
    def PluginIndex(self) -> Optional[int]:
        return self._other_elements.get('pluginIndex')
    @property
    def PluginName(self) -> Optional[str]:
        return self._other_elements.get('pluginName')
    @property
    def PluginType(self) -> Optional[int]:
        return self._other_elements.get('pluginType')
    @property
    def ReplacedClips(self) -> list:
        return self._replaced_clips
    @property
    def TransitionDirection(self) -> Optional[int]:
        return self._other_elements.get('transitionDirection')
    @property
    def TransitionSpeed(self) -> Optional[int]:
        return self._other_elements.get('transitionSpeed')


class VFXClip(VideoClip):
    """Subclass of VideoClip for tracking clips that had filters applied"""
    def __init__(self, clip_dict):
        required = {"duration","file","name","in","out","startFrame","track","framesTakenAfter","framesTakenBefore"}
        if not set(clip_dict.keys()).issuperset(required):
            raise ValueError(f"VideoClip is missing required elements {required.difference(set(clip_dict.keys()))}!")
        super().__init__(clip_dict)
        self._framesBefore = clip_dict['framesTakenBefore']
        self._framesAfter  = clip_dict['framesTakenAfter']
        self._startFrame   = clip_dict['startFrame']

        self._filtered_clips = [VideoClip(clip) for clip in clip_dict.get('filteredClips', [])]

    @property
    def ClipEatenByFilter(self) -> Optional[bool]:
        return self._other_elements.get('clipEatenByFilter')
    @property
    def FilterFadeInFrames(self) -> Optional[int]:
        return self._other_elements.get('filterFadeinFrames')
    @property
    def FilterFadeOutFrames(self) -> Optional[int]:
        return self._other_elements.get('filterFadeoutFrames')
    @property
    def FilterSliderValues(self) -> Optional[List[float]]:
        return self._other_elements.get('filterSliderValues')
    @property
    def FilteredClips(self) -> list:
        return self._filtered_clips
    @property
    def FramesTakenAfter(self) -> int:
        return self._framesAfter
    @property
    def FramesTakenBefore(self) -> int:
        return self._framesBefore
    @property
    def PluginIndex(self) -> Optional[int]:
        return self._other_elements.get('pluginIndex')
    @property
    def PluginName(self) -> Optional[str]:
        return self._other_elements.get('pluginName')
    @property
    def PluginType(self) -> Optional[int]:
        return self._other_elements.get('pluginType')
    @property
    def SolidColorClipColor(self) -> Optional[List[int]]:
        return self._other_elements.get('solidColorClipColor')

class iMovieProj:
    """Class to handle structure of an iMovieHD project
    """

    def __init__(self, xmldict:Dict[str, Any]):
        nested_keys = ["audioClips", "audioTrashClips", "videoClips", "videoTrashClips"]
        self._other_elements = {key:xmldict[key] for key in xmldict.keys() if key not in nested_keys}
        self._audioClips      = [AudioClip(aclip) for aclip in xmldict.get("audioClips", [])]
        self._audioTrashClips = [AudioClip(aclip) for aclip in xmldict.get("audioTrashClips", [])]
        self._videoClips      = [VideoClip(vclip) for vclip in xmldict.get("videoClips", [])]
        self._videoTrashClips = [VideoClip(vclip) for vclip in xmldict.get("videoClips", [])]

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
