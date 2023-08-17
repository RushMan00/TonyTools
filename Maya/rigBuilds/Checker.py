import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp

def checkIfFilePathsExist(filePath='D:/OneDrive/TonyTools'):
    # Check if the directory exists
    filePath = filePath.replace("\\", "/")  # replace backslashes with forward slashes
    if not os.path.exists(filePath):
        pm.warning(f"The directory {filePath} does not exist or path is not correct, "
                   f"please check Drive location and path location carefully :) ")
        return False
    print(f"The directory {filePath} exist!")
    return True

def checkIfObjectExist(obj_list=[]):
    for obj in obj_list:
        if not pm.objExists(obj):
            print(f"Object '{obj}' doesn't exist")
            return False

    print("Object(s) exist")
    return True

