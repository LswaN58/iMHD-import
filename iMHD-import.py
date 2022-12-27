import bpy

path_of_proj_file = "/Volumes/Little_Black_Box/LBB Users/LBB lukeswanson/LBB Movies/Outdoor_Movie/outdoor_movie_edit.iMovieProj"
path_of_clips = "/Volumes/Little_Black_Box/LBB Users/LBB lukeswanson/LBB Movies/Outdoor_Movie/"

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

class Project:
    """ Tracking of project-level properties
    """
    def __init__(self, x_res=640, y_res=480):
        self._x_res = x_res
        self._y_res = y_res

    @property
    def XResolution(self):
        return self._x_res
    @property
    def YResolution(self):
        return self._y_res