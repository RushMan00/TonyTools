import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp

def convertSlashesToDoubleBackslashes(inputPath=r'D:/OneDrive/TonyTools'):
    """
    Converts all forward slashes in the given path to double backslashes.

    Args:
    - input_path (str): The path with forward slashes.

    Returns:
    - str: The modified path with double backslashes.
    """
    # First, replace all single backslashes with double backslashes
    modifiedPath = inputPath.replace("\\", "\\\\")
    # Then, replace all forward slashes with double backslashes
    return modifiedPath.replace("/", "\\\\")

def checkIfFilePathsExist(filePath=r'D:/OneDrive/TonyTools'):
    """
    Checks if the given directory exists after converting its slashes to double backslashes.
    It also prints out a message based on the result and returns the existence status and the modified path.

    Args:
    - file_Path (str): The path to the directory. Default is 'D:/OneDrive/TonyTools'.

    Returns:
    - tuple: A tuple containing a boolean indicating the existence of the directory
             and the modified path string.

    Usage Example:
    exists, modified_path = Checker.checkIfFilePathsExist('D:/Example/Path')
    """
    filePath = convertSlashesToDoubleBackslashes(filePath)
    print(filePath)
    if not os.access(filePath, os.W_OK):
        print('Directory is not writable:', filePath)
        return False, filePath
    if not os.path.exists(filePath):
        print(f"The directory {filePath} does not exist or path is not correct. "
              f"Please check Drive location and path location carefully.")
        return False, filePath
    else:
        print(f"The directory {filePath} exists!")
        return True, filePath

def checkIfObjectExist(obj_list=[]):
    for obj in obj_list:
        if not pm.objExists(obj):
            print(f"Object '{obj}' doesn't exist")
            return False

    print("Object(s) exist")
    return True

def checkIfObjectExist2(objList=[]):
    for obj in objList:
        if not cmds.objExists(obj):
            print(f"Object '{obj}' doesn't exist")
            return False

    print("Object(s) exist")
    return True

def checkingSides(self):
    if self.side == 'C':
        self.side = 'C'
        if not self.color:
            self.color = 22
            self.__createControl()

    elif self.side == 'L':
        self.side = 'L'
        if not self.color:
            self.color = 4
            self.__createControl()

    elif self.side == 'R':
        self.side = 'R'
        if not self.color:
            self.color = 6
            self.__createControl()
    else:
        pm.warning('Please specify a "side".')
        return