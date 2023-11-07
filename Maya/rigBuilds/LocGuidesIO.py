import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp

from rigBuilds import BaseRig, Checker, attribute
imp.reload(BaseRig)
imp.reload(Checker)
imp.reload(attribute)

def selectTaggedNodes(tagName='myTag'):

    '''
    Selects all objects in the scene that have a specified tag attribute.

    Args:
        tagName (str): The name of the tag attribute to search for.

    Returns:
        list: A list of the selected objects with the specified tag attribute.

    Raises:
        None

    Examples:
        tagged_objects = selectTaggedNodes(tagName='joints')
        tagged_objects = selectTaggedNodes(tagName='customTag')

    Notes:
        - This function searches for objects of type 'transform' in the scene.
        - The tag attribute must be attached to the object using the `addAttr` command in Maya.
        - If no objects are found with the specified tag attribute, a warning message is displayed.
        - If objects with the specified tag attribute are found, they are selected and returned as a list.
        - Multiple objects can have the same tag attribute.

    Author: Tony K Song
    Date: 06/05/2023
    Version: 1.0.0
    '''

    # List all objects with the specified tag attribute
    taggedObjs = []
    for node in cmds.ls(type='transform'):
        if cmds.attributeQuery(tagName, node=node, exists=True):
            taggedObjs.append(node)

    if not taggedObjs:
        cmds.warning('No objects found with the tag attribute: {}'.format(tagName))
    else:
        # Return the tagged objects
        return taggedObjs

def writeLocGuidesData(tagName='node', filePath='\TonyTools\Maya\projects\pridapus\data'):
    '''
    Writes location guide data for tagged objects in the scene to a specified file path.

    Args:
        tagName (str): The name of the tag attribute to search for. Default is 'node'.
        filePath (str): The file path to write the location guide data to.

    Returns:
        None

    Raises:
        None

    Examples:
        writeLocGuidesData(tagName='node', filePath='/path/to/data/file.txt')
        writeLocGuidesData(tagName='customTag', filePath='/path/to/custom/data.txt')

    Notes:
        - This function relies on the 'selectTaggedNodes' function to get the tagged objects.
        - The function collects translation (tx, ty, tz) and rotation (rx, ry, rz) data for each tagged object.
        - The data is stored in a list of dictionaries, where each dictionary represents an object and its corresponding data.
        - The file path is expected to be a valid directory path where the data file will be written.
        - If the specified directory does not exist, a warning message is displayed, and the function exits.

    Author: Tony K Song
    Date: 06/05/2023
    Version: 1.0.0
    '''

    def selectTaggedNodes(tagName):
        taggedNodes = [node for node in cmds.ls(type='transform') if cmds.attributeQuery(tagName, node=node, exists=True)]
        return taggedNodes if taggedNodes else None

    # Find the LocGuides in the scene
    locs = selectTaggedNodes(tagName=tagName)
    if not locs:
        return

    dataList = []
    for obj in locs:
        dataDict = {}
        objName = cmds.ls(obj, long=True)[0]  # Get the full path name of the object
        dataDict[objName] = {
            "tx": cmds.getAttr(f"{obj}.translateX"),
            "ty": cmds.getAttr(f"{obj}.translateY"),
            "tz": cmds.getAttr(f"{obj}.translateZ"),
            "rx": cmds.getAttr(f"{obj}.rotateX"),
            "ry": cmds.getAttr(f"{obj}.rotateY"),
            "rz": cmds.getAttr(f"{obj}.rotateZ")
        }
        dataList.append(dataDict)

    # Check if the directory exists
    filePath = filePath.replace("\\", "/")  # replace backslashes with forward slashes
    if not os.path.exists(filePath):
        cmds.warning(f"The directory {filePath} does not exist.")
        return

    # Save data to JSON file
    filePath = os.path.join(filePath, 'locGuideData.json')
    with open(filePath, 'w') as json_file:
        json.dump(dataList, json_file, indent=4)

    return dataList

def loadLocGuidesData(filePath='\TonyTools\Maya\projects\pridapus\data'):

    '''
    Loads location guide data from a specified file path and applies it to corresponding objects in the scene.

    Args:
        filePath (str): The file path to load the location guide data from.

    Returns:
        dataList (list): A list containing the loaded location guide data in dictionary format.

    Raises:
        None

    Examples:
        loadLocGuidesData(filePath='/path/to/data/locGuideData.json')
        loadLocGuidesData(filePath='/path/to/custom/data.json')

    Notes:
        - The function loads location guide data from a JSON file.
        - The file path is expected to be a valid directory path where the data file is located.
        - The file name is assumed to be 'locGuideData.json' and is appended to the provided file path.
        - If the specified file does not exist, a warning message is displayed, and the function exits.
        - The location guide data is expected to be in a list of dictionaries format.
        - Each dictionary represents an object and its corresponding attribute values.
        - The function iterates over the data, sets the attribute values on the corresponding objects,
          and handles cases where attributes are locked or connected to other attributes.
        - If any attribute fails to be set, an appropriate message is displayed.
        - The function returns the loaded location guide data as a list.

    Author: Tony K Song
    Date: 06/05/2023
    Version: 1.0.0
    '''

    print('---- STARTING to load in LocGuides Data ----')

    # Assuming 'Checker.checkIfFilePathsExist' is a valid function that returns a tuple
    exists, filePaths = Checker.checkIfFilePathsExist(filePath)
    filePaths = os.path.join(filePaths, 'locGuideData.json')

    with open(filePaths, 'r') as json_file:
        dataList = json.load(json_file)

    for num, data in enumerate(dataList):
        for nodeName, attrs in data.items():
            print(nodeName)
            for axis, val in attrs.items():
                attrName = '{}.{}'.format(nodeName, axis)
                if cmds.getAttr(attrName, lock=True):
                    print(f"The attribute {attrName} is locked.")
                    continue
                else:
                    try:
                        cmds.setAttr(attrName, val)
                    except RuntimeError:
                        print(
                            f"Could not set value for attribute {attrName}.\n"
                            "It may be connected to another attribute.")
                        continue

    print('---- Finished loading in LocGuides Data ----')
    return dataList
