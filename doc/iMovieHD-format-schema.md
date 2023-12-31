# Documentation of the iMovie HD project xml format

This document specifies the structure of an `.iMovieProj` XML file.
Each element has the format:

- `key` : **value type** ~ *example value*  
    Description of value

Arrays are given *example value* of *[...]*, because we're not typing out a full example array.
Similarly, dictionaries are given *example value* of *{...}*.

General formatting hierarchy is as follows:

- audioClips : []
    - `class` : **enum(audio)** ~ *audio*  
        The 'class' of the clip, in this case always `audio`.
    - `duration` : **int** ~ *3*  
        Not yet known
    - `file` : **string** ~ *"Sound 01.aiff"*  
        Name of the source file imported/rendered and shown in timeline
    - `imae4cc` : **int** ~ *0*  
        Not yet known
    - `imaeFilteredList` : **array** *[...]*
        - audioClip, basically recursive definition
    - `imaeVersion` : **int** ~ *0*  
        Not yet known
    - `in` : **int** ~ *0*  
        The frame of the source file at which the clip begins
    - `isSelected` : **bool** ~ *`<true/>`*  
        A boolean indicating whether the clip is selected in the editor
    - `name` : **string** ~ *"Sound 01"*  
        The in-editor name of the clip
    - `out` : **int** ~ *94*  
        The frame of the source file at which the clip ends
    - `pushPins` : **array[dict]** ~ *[ {...}, ...]*
        - `audioFrame` : **int** ~ 0  
            Not yet known
        - `clipUID` : **int** ~ *1*  
            Not yet known
        - `originalClipFrame` : **int** ~ *-1*  
            Not yet known
        - `originalClipUID` : **int** ~ *-1*  
            Not yet known
        - `videoFrame` : **int** ~ *12*  
            Not yet known
    - `startFrame` : **int** ~ *89*  
        The frame of the project edit at which the clip begins
    - `timeScale` : **int** ~ *2997*  
        The framerate of the clip
    - `track` : **int** ~ *2*  
        The audio channel where the clip sits in the edit
    - `trimmedEndFrame` : **int** ~ *94*  
        Not yet known, presumed to be the frame of the source file at which the clip ends
    - `trimmedStartFrame` : **int** ~ *0*
        Not yet known, presumed to be the frame of the source file at which the clip begins
    - `uniqueID` : **int**
    - `version` : **string**  
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
