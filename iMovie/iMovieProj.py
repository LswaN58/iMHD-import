from pathlib import Path
from typing import Any, Dict, List, Optional
# local imports
from iMovie.AudioClip import AudioClip
from iMovie.TopVideoClip import TopVideoClip, TopVideoClipFactory

class iMovieProj:
    """Class to handle structure of an iMovieHD project
    """

    def __init__(self, xmldict:Dict[str, Any]):
        nested_keys = ["audioClips", "audioTrashClips", "videoClips", "videoTrashClips"]
        self._other_elements  : Dict[str, Any]  = {key:xmldict[key] for key in xmldict.keys() if key not in nested_keys}
        self._audioClips      : List[AudioClip] = [AudioClip(aclip) for aclip in xmldict.get("audioClips", [])]
        self._audioTrashClips : List[AudioClip] = [AudioClip(aclip) for aclip in xmldict.get("audioTrashClips", [])]
        self._videoClips      : List[TopVideoClip] = [TopVideoClipFactory.FromDict(vclip) for vclip in xmldict.get("videoClips", [])]
        self._videoTrashClips : List[TopVideoClip] = [TopVideoClipFactory.FromDict(vclip) for vclip in xmldict.get("videoClips", [])]

    def __repr__(self) -> str:
        return f"iMovieProj object: {len(self.VideoClips)} video clips; {len(self.AudioClips)} audio clips; {self.VideoStandard} format"

    @staticmethod
    def FromXMLFile(file:Path):
        xmldict = XMLDict.LoadXMLDict(file)
        project : iMovieProj     = iMovieProj(xmldict=xmldict)

        print(f"""
        ***
        Results from importing {file}:
            project: {project}
            VideoClips: {project.VideoClips}
            AudioClips: {project.AudioClips}

        ***

        """)

        return project

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
    def VideoClips(self) -> List[TopVideoClip]:
        return self._videoClips
    @property
    def VideoStandard(self) -> Optional[str]:
        return self._other_elements.get("videoStandard")
    @property
    def VideoTrashClips(self) -> List[TopVideoClip]:
        return self._videoTrashClips
    @property
    def WritingApplicationName(self) -> Optional[str]:
        return self._other_elements.get("writingApplicationName")
    @property
    def WritingApplicationVersion(self) -> Optional[str]:
        return self._other_elements.get("writingApplicationVersion")