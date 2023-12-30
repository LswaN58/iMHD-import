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

### Standard Elements

#### Identifier Elements

- `class`
    Always "audio"
- `file`
- `name`
    This is usually just the same string as `file`, but without a file extension.
    Could be a different name if the clip has an effect applied, in which case a new clip is rendered with the clip and a new name based on effect type.

#### Timing Elements

- `duration`
- `in`
- `out`
- `startFrame`
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

#### Unknown Elements

- `imae4cc`
- `imaeVersion`
- `imaeFilteredList`

### Recursive Elements


## <a name="videoclips">Video Clips</a>

## Effect Clips
