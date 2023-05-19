import maya.cmds as cmds
import pymel.core as pm
import json
import os

def selectTaggedNodes(tagName='myTag'):
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
                    print(axis, val)
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