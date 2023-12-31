# iMovie HD Project File Format

## Big-Picture Organization

iMovieHD project files are XML files (gross) that define a collection of audio, video, and effects clips.

At the most basic root level, these files simply define an XML header, a `plist`, and a single `dict` inside the `plist`.
Obviously, all the interesting stuff is inside the `dict`.

> Note: XML `dict`s (at least as used here) are pretty awful; they are made up of a series of paired `<key>` and value elements, where the `<key>` element has a literal tag of "`<key>`" and the values have tags of some type, e.g. "`<string>`" or "`integer`"

### iMovieHD Top-Level `dict` Element

The top-level dict contains a number of elements, most of which are used for recording the state of the editor, rather than the edit.
For example, the `timelineZoom` or `relativePlayHeadPosition` keys.

The elements that define the edit itself are mostly nested as sub-elements within a few specific elements.
There are also a few elements containing metadata about the program that created the file.
The different categories are given below:

#### Editor State Elements

These are elements that appear to relate to the state of the editor at the time the file was saved.
Most are self-explanatory in their naming; I've added comments where the names are unclear.

- `lastClipUniqueID`
- `playheadPosition`
- `relativePlayHeadPosition`
- `selectionEndFrame`
- `selectionStartFrame`
- `selectionType`  
    This is an integer, probably representing an enum.
    However, I don't yet have enough examples to know what the int->enum mapping is.
- `timelineZoom`

#### File Metadata Elements

As above, I've made notes where the name may not be sufficient to understand the meaning of the element.
Note there are two "versioning" elements, namely `version` and `writingApplicationVersion`.
I'm not sure what differs between these.
My assumption would be that `version` is a version of the `.iMovieProj` spec, and `writingApplicationVersion` is the application version (duh).
However, I have no way to know this for sure.
In any case, I've only ever used exactly one major version of iMovieHD (that I know of), so don't have examples where the versioning actually differs from `4.1` and `6.0`, respectively.

- `version`
- `videoStandard`  
    This is the file format of the project, e.g. "MPEG"
    When iMovieHD imports clips of whatever input format the source footage is in, it converts them to the format of the `videoStandard`.
- `writingApplicationName`  
    To the best of my knowledge, this is just the string "iMovie".
    It's possible this XML-based project format was used across Apple editing software back then.
- `writingApplicationVersion`

#### Edit State Elements

These will be discussed in much more detail in the sections on [Audio Clips](#audioclips) and [Video Clips](#videoclips)

- `audioClips`
- `audioTrashClips`
- `videoClips`
- `videoTrashClips`

## <a name="audioclips">Audio Clips</a>

Here we get to the meat of the file.
The `audioClips` key is mapped to an `array`.
The array elements are `dict`s, each with a complex bunch of sub-elements.

Full descriptions of the elements are in the `iMovieHD_file-spec`, but a summary description of the broad categories is here.

### Standard Elements - Audio

#### Identifier Elements - Audio

These elements identify the given audio clip and its source.
Note there are `file` and `name` elements.
The `file` element is the name of the file used in the editor, which is always an imported file, or a rendered file, not the original source that was imported.
The `name` is usually just the same string as `file`, but without a file extension.
However, this can vary a bit.  

> Example : If a clip has been split, each part will have the same `file` name, say `"aud.aiff"`.
> However, they will have suffixes indicating which part of the split they were, say `"aud/1"` and `"aud/2"`.

> Example : If a clip was created by rendering an effect, the `file` name may be, say `"Effect 01.aif"`.
> The `name` element, however, may be named for the effect alone, say `Effect`

- `class`
    Always "audio"
- `file`
- `name`
- `uniqueID`
- `version`
    I'm not really sure what this version refers to, although in the test files I've reviewed, this is always `4`, similar to how the file metadata `version` is always `4.1`.
    Thus, this probably is just the major version of the spec, or whatever the file's `version` refers to.

#### Edit State Elements - Audio

These elements define the edit for an individual audio clip.
To the best of my knowledge, the `in` and `out` refer to when the clip begins and ends *within the source file*.
The `duration` appears to be the length of the source file, and `startFrame` is presumably the frame of the overall edit at which the audio clip is placed.
I am not certain about the `trimmedStartFrame` and `trimmedEndFrame`; in the simple example files I've worked with, these appear redundant with `in` and `out`

> Example : Assume a source for the audio clip called `aud.aiff`.
> Assume the clip element has `in = 25`, `out = 40`, `duration = 100`, `startFrame = 10`.
> Then the audio clip begins in the 10th frame of the edit, with a duration within the edit of 15 frames.
> Those frames are the 25th through 40th frames of the `aud.aiff` file.

- `duration`
- `in`
- `out`
- `startFrame`
- `trimmedEndFrame`
- `trimmedStartFrame`
- `timeScale`
    This is the FPS of the clip, which I believe is defined by the project.  
    Note that it *is* an integer, so a 29.97 would have value of 2997.
    Perhaps best to treat more like an enum, in that case.
- `pushPins`
    This is an array, where each element is itself a dictionary.
    These contain subelements to define where a push-pin was placed to set the clip volume, I believe.
    - `audioFrame`
    - `clipUID`
    - `originalClipFrame`
    - `originalClipUID`
    - `videoFrame`
    I haven't yet worked out what they each mean.

#### Editor State Elements - Audio

- `isSelected`
- `track`
    This appears to just be the audio channel of the editor where the clip sits.

#### Unknown Elements - Audio

I think `imae` is related to the effects/plugins engine, but don't really know what these elements are for.

- `imae4cc`
- `imaeVersion`
- `imaeFilteredList`

### Recursive Elements - Audio


## <a name="videoclips">Video Clips</a>

### Standard Elements - Video

#### Identifier Elements - Video

These elements identify the given audio clip and its source.
Note there are `file` and `name` elements.
The `file` element is the name of the file used in the editor, which is always an imported file, or a rendered file, not the original source that was imported.
The `name` is usually just the same string as `file`, but without a file extension.
However, this can vary a bit.  

> Example : If a clip has been split, each part will have the same `file` name, say `"vid.mov"`.
> However, they will have suffixes indicating which part of the split they were, say `"vid/1"` and `"vid/2"`.

#### Timing Elements - Video


#### Editor State Elements - Video


#### Unknown Elements - Video


### Recursive Elements - Video

## Effect Clips
