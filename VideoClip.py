# builtin imports
from typing import Any, Dict, List, Optional, Set, Union

class VideoClip:
    """Tracking of video clip properties"""
    def __init__(self, clip_dict, sub_required:Set[str]):
        if not clip_dict.get('class') == "video":
            raise ValueError(f"VideoClip constructor was given a dict of class {clip_dict.get('class')}!")
        required = sub_required.union({"duration","file","name","in","out","track"})
        if not set(clip_dict.keys()).issuperset(required):
            raise ValueError(f"VideoClip is missing required elements {required.difference(set(clip_dict.keys()))}!")
        self._duration     = clip_dict['duration']
        self._fileName     = clip_dict['file']
        self._name         = clip_dict['name']
        self._inFrame      = clip_dict['in']
        self._outFrame     = clip_dict['out']
        self._track        = clip_dict['track']

        self._other_elements = {clip:clip_dict[clip] for clip in clip_dict.keys() if clip not in required}

    def __repr__(self):
        return f"VideoClip object: name {self.Name}; file {self.FileName}; start {self.InFrame}; end {self.OutFrame}"
    def __str__(self):
        return self.__repr__()

    #region Props not for direct access
    @property
    def IsFiltered(self) -> bool:
        return True
    @property
    def FilterDepth(self) -> int:
        return 0
    @property
    def BaseFileName(self) -> Union[str, List[str]]:
        return self.FileName
    @property
    def InEdit(self):
        """Method to check if the current clip is part of the edit."""
        if self._track == 0:
            return False
        elif self._track == 1:
            return True
        else:
            return False
    #endregion

    #region Props for direct access to dict items
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
    def Volume(self) -> float:
        return self._other_elements.get('volume', 1.0)
    #endregion

class FilteredClip(VideoClip):
    """Class for all the things not in VideoClip, but common to VFX and Transitions."""
    def __init__(self, clip_dict, sub_required:Set[str]):
        required = sub_required.union({"framesTakenAfter","framesTakenBefore"})
        super().__init__(clip_dict, sub_required=required)
        self._framesBefore = clip_dict['framesTakenBefore']
        self._framesAfter  = clip_dict['framesTakenAfter']

    @property
    def IsFiltered(self) -> bool:
        return True

    #region Props for direct access to dict items
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
    #endregion

class Transition(FilteredClip):
    """Subclass of VideoClip to handle info about Transitions"""
    def __init__(self, clip_dict):
        required = {"replacedClips"}
        super().__init__(clip_dict, sub_required=required)
        self._replaced_clips = [VideoClipFromDict(clip) for clip in clip_dict.get('replacedClips', [])]

    @property
    def BaseFileName(self) -> Union[str, List[str]]:
        ret_val = []
        base_list = [clip.BaseFileName for clip in self.ReplacedClips]
        for item in base_list:
            if isinstance(item, str):
                ret_val.append(item)
            elif isinstance(item, list):
                ret_val += item
        return ret_val

    @property
    def ReplacedClips(self) -> List[VideoClip]:
        return self._replaced_clips
    @property
    def TransitionDirection(self) -> Optional[int]:
        return self._other_elements.get('transitionDirection')
    @property
    def TransitionSpeed(self) -> Optional[int]:
        return self._other_elements.get('transitionSpeed')

class VFXClip(FilteredClip):
    """Subclass of VideoClip for tracking clips that had filters applied"""
    def __init__(self, clip_dict):
        super().__init__(clip_dict, sub_required={"startFrame"})
        self._startFrame   = clip_dict['startFrame']

        self._filtered_clips = [VideoClipFromDict(clip) for clip in clip_dict.get('filteredClips', [])]

    def __repr__(self) -> str:
        return f"VFXClip object: Subclass of {super(VFXClip, self).__repr__()}; Plugin {self.PluginName}; {len(self.FilteredClips)} filtered clip(s); Base file {self.BaseFileName}"

    @property
    def FilterDepth(self) -> int:
        return 0 if self.FilteredClips == [] else (self.FilteredClips[0].FilterDepth + 1)

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
    def FilteredClips(self) -> List[VideoClip]:
        return self._filtered_clips
    @property
    def StartFrame(self) -> int:
        return self._startFrame
    @property
    def SolidColorClipColor(self) -> Optional[List[int]]:
        return self._other_elements.get('solidColorClipColor')

def VideoClipFromDict(clip_dict) -> VideoClip:
    if clip_dict.get('class') == "transition":
        return Transition(clip_dict=clip_dict)
    elif clip_dict.get('clipEatenByFilter') is True:
        return VFXClip(clip_dict=clip_dict)
    else:
        return VideoClip(clip_dict=clip_dict, sub_required=set())