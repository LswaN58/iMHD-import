from xml.etree.ElementTree import ElementTree, Element

class VideoClip:
    """Tracking of video clip properties"""
    def __init__(self):
        self._duration = 0
        self._fileName = "empty"
        self._sceneName = "empty"
        self._inFrame = 0
        self._outFrame = 0
        self._partOfEdit = 0

    @property
    def Duration(self):
        """Method to check the clip's file name"""
        return self._duration

    @property
    def FileName(self):
        """Method to check the clip's file name"""
        return self._fileName

    @property
    def SceneName(self):
        """Method to check the clip's scene name"""
        return self._sceneName

    @property
    def InFrame(self):
        """Method to check the clip's file name"""
        return self._inFrame

    @property
    def OutFrame(self):
        """Method to check the clip's scene name"""
        return self._outFrame

    @property
    def InEdit(self):
        """Method to check if the current clip is part of the edit."""
        if self._partOfEdit == 0:
            return False
        elif self._partOfEdit == 1:
            return True
        else:
            return False

    def toString(self):
        return "scene " + self._sceneName + ", file " + self._fileName + ", in edit: " + str(self._partOfEdit)

class iMovieProj:
    @staticmethod
    def XMLTreeToDict(xmltree:ElementTree):
        root = xmltree.getroot()
        if len(root) > 1:
            # file should have only one dict
            raise ValueError(f"Expected only one element (a dict) under iMovieProj XML root, found {len(root)}!")
        xmldict = root[0]
        if xmldict.tag != "dict":
            raise ValueError(f"Expected a dict under iMovieProj XML root, found {xmldict.tag}!")
        return iMovieProj._parseDict(xmldict)

    @staticmethod
    def _parse(xmlvalue:Element):
        if xmlvalue.tag == "true":
            return True
        elif xmlvalue.tag == "false":
            return False
        else:
            if xmlvalue.text == None:
                raise ValueError(f"Expected XML Element with tag {xmlvalue.tag} to have a value, but found a value of None!")
            elif xmlvalue.tag == "string":
                return str(xmlvalue.text)
            elif xmlvalue.tag == "integer":
                return int(xmlvalue.text)
            elif xmlvalue.tag == "real":
                return float(xmlvalue.text)
            elif xmlvalue.tag == "array":
                return [iMovieProj._parse(elem) for elem in xmlvalue]
            elif xmlvalue.tag == "dict":
                return iMovieProj._parseDict(xmlvalue)

    @staticmethod
    def _parseDict(xmldict:Element):
        ret_val = {}

        if len(xmldict) % 2 != 0:
            raise ValueError(f"Expected the XML dictionary to have an even number of elements, found {len(xmldict)} elements!")
        for i in range(len(xmldict) // 2):
            if xmldict[2*i].tag != "key":
                raise ValueError(f"Expected the even keys under XML dict to be keys, found element {2*i} with tag {xmldict[2*i].tag}!")
            key = xmldict[2*i].text
            val = iMovieProj._parse(xmldict[2*i + 1])
            ret_val[key] = val

        return ret_val

    def __init__(self, xmldict):

        self._audioClips = self._getAudioClips(xmltree)
        self._audioTrashClips = self._getAudioTrashClips(xmltree)
        self._lastClipUniqueID = 