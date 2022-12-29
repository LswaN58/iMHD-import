# 3rd-party imports
import bpy
# local imports
from importer import iMovieProj, VideoClip, AudioClip

class Blender:
    """Class to handle setting up stuff within Blender"""
    @staticmethod
    def SetupEditFromiMovieProj(proj:iMovieProj):
        bpy.context.scene = main_scene

    @staticmethod
    def CreateVideoStrip(clip:VideoClip):
        pass

    @staticmethod
    def CreateVideoScene(clip:VideoClip):
        bpy.ops.scene.new(type='NEW')
        current_scene = bpy.context.scene
        current_scene.name = clipObj.sceneName
        current_scene.frame_start = clipObj.inFrame
        current_scene.frame_end = clipObj.outFrame
        current_scene.render.resolution_x = x_res
        current_scene.render.resolution_y = y_res
        current_scene.render.resolution_percentage = 100
        current_scene.render.fps = 30
        current_scene.render.fps = 1.001
        ### Open Clip and add it to compositor
        print("in make new: " + clipObj.toString())
        bl_open_clip(clipObj, path_of_clips)
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links
        #Set up node tree
        tree.nodes.remove(tree.nodes["Render Layers"])
        clip_node = tree.nodes.new(type="CompositorNodeMovieClip")
        viewer_node = tree.nodes.new(type="CompositorNodeViewer")
        #Link them
        links.new(clip_node.outputs[0], viewer_node.inputs[0])
        bpy.ops.sequencer.scene_strip_add(frame_start=start_frame, channel=1, scene=clip_name)
        return

    @staticmethod
    def CreateAudioStrip(clip:AudioClip):
        pass