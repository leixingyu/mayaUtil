import maya.cmds as cmds
import maya.mel as mel


def get_timeline_range():
    """ Get timeline full range and truncated range

    :return: full range and truncated range
    :rtype: list, list
    """

    # maya full timeline range
    full_min = cmds.playbackOptions(animationStartTime=1, q=1)
    full_max = cmds.playbackOptions(animationEndTime=1, q=1)

    # truncated timeline range
    trunc_min = cmds.playbackOptions(minTime=1, q=1)
    trunc_max = cmds.playbackOptions(maxTime=1, q=1)

    return [full_min, full_max], [trunc_min, trunc_max]


def attach_audio(name):
    """ Attach the audio to the timeline

    :param name: audio name
    :type name: string
    """

    audios = cmds.ls(type='audio')
    if name in audios:
        playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
        cmds.timeControl(playback_slider, sound=name, displaySound=1, e=1)
    else:
        return
