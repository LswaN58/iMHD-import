from typing import Any, Dict, List, Optional, Set, Union
from VideoClip import VideoClip
from NestedVideoClip import NestedVideoClipFactory

Map = Dict[str, Any]

class TopVideoClip(VideoClip):
    """Class for clips that come from a video file."""
    def __init__(self, clip_dict:Map, sub_required:Set[str]):
        required = sub_required.union({"track"})
        super().__init__(clip_dict, sub_required=required)
        self._track  = clip_dict['track']

    def __repr__(self):
        return f"<TopVideoClip object: Subclass of {super(TopVideoClip, self).__repr__()}>"

    @property
    def Track(self) -> str:
        return self._track

class TopVideoFileClip(TopVideoClip):
    """Class for clips that come from a video file."""
    def __init__(self, clip_dict:Map, sub_required:Set[str]):
        required = sub_required.union({"file"})
        super().__init__(clip_dict, sub_required=required)
        self._fileName  = clip_dict['file']

    def __repr__(self):
        return f"<VideoFileClip object: Subclass of {super(TopVideoFileClip, self).__repr__()}; File {self.FileName}>"

    @property
    def BaseFileName(self) -> Union[str, List[str]]:
        return self.FileName

    @property
    def FileName(self) -> str:
        return self._fileName

class TopFilteredClip(TopVideoFileClip):
    """Class for all the things not in VideoClip, but common to VFX and Transitions."""
    def __init__(self, clip_dict:Map, sub_required:Set[str]):
        required = sub_required.union({"framesTakenAfter","framesTakenBefore"})
        super().__init__(clip_dict, sub_required=required)
        self._framesBefore = clip_dict['framesTakenBefore']
        self._framesAfter  = clip_dict['framesTakenAfter']

    def __repr__(self):
        return f"<FilteredClip object: Subclass of {super(TopFilteredClip, self).__repr__()}; Plugin {self.PluginName}>"

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

class TopTransition(TopFilteredClip):
    """Subclass of VideoClip to handle info about Transitions"""
    def __init__(self, clip_dict:Map):
        required = {"replacedClips"}
        super().__init__(clip_dict, sub_required=required)
        self._replaced_clips = [NestedVideoClipFactory.FromDict(clip) for clip in clip_dict.get('replacedClips', [])]

    def __repr__(self):
        return f"<Transition object: subclass of {super(TopTransition, self).__repr__()}; {len(self.ReplacedClips)} replaced clip(s); Base file(s) of {self.BaseFileName}>"

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

class TopVFXClip(TopFilteredClip):
    """Subclass of VideoClip for tracking clips that had filters applied"""
    def __init__(self, clip_dict:Map):
        super().__init__(clip_dict, sub_required={"startFrame"})
        self._startFrame   = clip_dict['startFrame']

        self._filtered_clips = [NestedVideoClipFactory.FromDict(clip) for clip in clip_dict.get('filteredClips', [])]

    def __repr__(self) -> str:
        return f"<VFXClip object: Subclass of {super(TopVFXClip, self).__repr__()}; {len(self.FilteredClips)} filtered clip(s); Base file {self.BaseFileName}>"

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

class TopVideoClipFactory:
    @staticmethod
    def FromDict(clip_dict) -> TopVideoClip:
        if clip_dict.get('class') == "transition":
            return TopTransition(clip_dict=clip_dict)
        elif clip_dict.get('clipEatenByFilter') is True:
            return TopVFXClip(clip_dict=clip_dict)
        else:
            return TopVideoClip(clip_dict=clip_dict, sub_required=set())