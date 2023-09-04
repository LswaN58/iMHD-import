# builtin imports
from typing import Any, Dict, List, Optional

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
        # Check if class is ok
        if not clip_dict.get('class') == "audio":
            raise ValueError(f"AudioClip constructor was given a dict of class {clip_dict.get('class')}!")
        # Check if clip got all necessary elements
        required = {"duration","file","name","in","out","startFrame","track","trimmedEndFrame","trimmedStartFrame"}
        available = set(clip_dict.keys())
        if not set(clip_dict.keys()).issuperset(required):
            vals_found = {key:clip_dict[key] for key in available.intersection(required)}
            msg = f"AudioClip is missing required elements {required.difference(available)}!\n   Found required elements {vals_found}"
            raise ValueError(msg)
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

    def __repr__(self):
        return f"<AudioClip object: name {self.Name}; file {self.FileName}; in {self.InFrame}; out {self.OutFrame}; start {self.StartFrame}>"
    def __str__(self):
        return self.__repr__()

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