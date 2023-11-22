import pymel.core as pm
import maya.cmds as cmds
import importlib

from rigBuilds import Checker
importlib.reload(Checker)


def loadMaFile(filepath):
    """
    Loads a Maya ASCII (.ma) file into the current Maya session.
    Returns True if the file was loaded successfully, False otherwise.
    """
    paths = None
    try:
        bools, paths = Checker.checkIfFilePathsExist(filepath)
        cmds.file(paths, i=True, type="mayaAscii", ignoreVersion=True, ra=True)

        return True
    except:
        cmds.warning("Failed to load file or path is not existing: {}".format(paths))
        return False