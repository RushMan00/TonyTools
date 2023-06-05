import maya.cmds as cmds
import pymel.core as pm
import json
import os

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

    # list all objects with the specified tag attribute
    taggedObjs = []
    for node in pm.ls(type='transform'):
        if node.hasAttr(tagName):
            taggedObjs.append(node)
    if not taggedObjs:
        pm.warning('No objects found with the tag attribute: {}'.format(tagName))
    else:
        # select the tagged objects
        # pm.select(taggedObjs)
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

    # find the LocGuides in the scene
    locs = selectTaggedNodes(tagName=tagName)
    if not locs:
        return
    dataList = []

    for obj in locs:
        dataDict = {}
        dataDict[obj.name()] = {
                                "tx": obj.tx.get(),
                                "ty": obj.ty.get(),
                                "tz": obj.tz.get(),
                                "rx": obj.rx.get(),
                                "ry": obj.ry.get(),
                                "rz": obj.rz.get()
                                }
        dataList.append(dataDict)
    print(dataList)

    # Check if the directory exists
    filePath = filePath.replace("\\", "/")  # replace backslashes with forward slashes
    if not os.path.exists(filePath):
        pm.warning(f"The directory {filePath} does not exist.")
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

    filePath = filePath.replace("\\", "/")  # replace backslashes with forward slashes
    filePath = os.path.join(filePath, 'locGuideData.json')

    if not os.path.exists(filePath):
        pm.warning(f"The file {filePath} does not exist.")
        return

    with open(filePath, 'r') as json_file:
        dataList = json.load(json_file)

    for num, data in enumerate(dataList):
        for nodeName, attrs in data.items():
            print(nodeName)
            # convert nodeName string to PyNode
            node = pm.PyNode(nodeName)
            for axis, val in attrs.items():
                # print(axis, val)
                if node.attr(axis).isLocked():
                    print(f"The attribute {nodeName}.{axis} is locked.")
                    continue
                else:
                    try:
                        pm.setAttr('{}.{}'.format(nodeName, axis), val)
                    except RuntimeError:
                        print(
                            f"Could not set value for attribute {nodeName}.{axis}. It may be connected to another attribute.")
    return dataList