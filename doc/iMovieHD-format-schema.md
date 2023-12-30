# Documentation of the iMovie HD project xml format

General formatting hierarchy is as follows:

- audioClips : []
  - class : enum(audio)
  - duration : int
  - file : string, name of modified file rendered and put in timeline
  - imae4cc : int
  - imaeFilteredList : []
    - audioClip, basically recursive definition
  - imaeVersion : int
  - in : int
  - isSelected : bool
  - name : string
  - out : int
  - pushPins : []
    - audioFrame : int
    - clipUID : int
    - originalClipFrame : int
    - originalClipUID : int
    - videoFrame : 12
  - startFrame : int
  - timeScale : int
  - track : int
  - trimmedEndFrame : int
  - trimmedStartFrame : int
  - uniqueID : int
  - version : string  
- audioTrashClips : []
- lastClipUniqueID : int
- playheadPosition : int
- relativePlayHeadPosition : float
- selectionEndFrame : int
- selectionStartFrame : int
- selectionType : int
- timelineZoom : float
- version : string
- videoClips : []
  - video example:
    - class : enum(transition, video)
    - duration : int
    - file : string, name of modified file rendered and put in timeline (if an effect)
    - in : int
    - isSelected : bool
    - mediaHandlePost : int
    - name : string
    - out : int
    - shelfX : int
    - shelfY : int
    - thumb : int
    - timeScale : int
    - track : int, but not included in filteredClips nested definitions
    - type : int, representing an enum(1=video_file, 2=transition, 5=generated_blank_screen)
    - uniqueID : int
    - version : string
  - video example with VFX:
    - class : enum(transition, video), video example below:
    - clipEatenByFilter : bool
    - duration : int
    - file : string, name of modified file rendered and put in timeline (if an effect)
    - filterFadeinFrames : int
    - filterFadeoutFrames
    - filterSliderValues : [float, float, float]
    - filteredClips : [ videoClip, basically recursive definition ]
    - framesTakenAfter : int
    - framesTakenBefore : int
    - in : int
    - isSelected : bool
    - mediaHandlePost : int
    - name : string
    - out : int
    - pluginIndex : int
    - pluginName : string
    - pluginType : int
    - shelfX : int
    - shelfY : int
    - solidColorClipColor : [int, int, int]
    - thumb : int
    - timeScale : int
    - track : int, but not included in filteredClips nested definitions
    - type : int
    - uniqueID : int
    - version : string
  - transition example:
    - class : enum(transition, video), transition example below:
    - duration : int
    - file : string, name of rendered transition
    - framesTakenAfter : int
    - framesTakenBefore : int
    - in : int
    - isSelected : bool
    - mediaHandlePost : int
    - name : string
    - out : int
    - pluginIndex : int
    - pluginName : string, technically an enum of transition types
    - pluginType : int
    - replacedClips : [ videoClip, basically recursive definition ]
    - thumb : int
    - timescale : int
    - track : int
    - transitionDirection : int
    - transitionSpeed : float
    - type : int
    - uniqueID : int
    - version : string
- videoStandard : str
- videoTrashClips : []
- writingApplicationName : string
- writingApplicationVersion : string