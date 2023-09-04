# builtin imports
from typing import Any, Dict, Optional, Set
class VideoClip:
    """Tracking of video clip properties"""
    def __init__(self, clip_dict:Dict[str, Any], sub_required:Set[str]):
        required = sub_required.union({"duration","name","in","out","uniqueID"})
        available = set(clip_dict.keys())
        if not available.issuperset(required):
            vals_found = {key:clip_dict[key] for key in available.intersection(required)}
            msg = f"VideoClip is missing required elements {required.difference(available)}!\n   Found required elements {vals_found}"
            raise ValueError(msg)
        self._duration  = clip_dict['duration']
        self._name      = clip_dict['name']
        self._inFrame   = clip_dict['in']
        self._outFrame  = clip_dict['out']
        self._unique_id = clip_dict['uniqueID']

        self._other_elements = {clip:clip_dict[clip] for clip in clip_dict.keys() if clip not in required}

    def __repr__(self):
        return f"<VideoClip object: name {self.Name}; start {self.InFrame}; end {self.OutFrame}>"
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
    def InEdit(self):
        """Method to check if the current clip is part of the edit."""
        if self.Track is None or self.Track == 0:
            return False
        elif self.Track >= 1:
            return True
        else:
            return False
    #endregion

    #region Props for direct access to dict items
    @property
    def Duration(self) -> int:
        return self._duration
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
    def Track(self) -> Optional[int]:
        return self._other_elements.get('track')
    @property
    def Type(self) -> Optional[int]:
        return self._other_elements.get('type')
    @property
    def UniqueID(self) -> Optional[bool]:
        return self._unique_id
    @property
    def Version(self) -> Optional[str]:
        return self._other_elements.get('version')
    @property
    def Volume(self) -> float:
        return self._other_elements.get('volume', 1.0)
    #endregion
