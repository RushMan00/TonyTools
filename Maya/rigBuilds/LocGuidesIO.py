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

def writeLocGuidesData(tagName='node', filePath = '\something'):
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
    directory = os.path.dirname(filePath)
    if not os.path.exists(directory):
        pm.warning(f"The directory {directory} does not exist.")
        return

    filePath = os.path.join(directory, 'locGuideData.json')

    # Save data to JSON filex
    with open(filePath, 'w') as json_file:
        json.dump(dataList, json_file, indent=4)

    return dataList

def loadLocGuidesData(filePath='\something'):
    filePath = filePath.replace("\\", "/")
    filePath = os.path.join(filePath, 'locGuideData.json')

    if not os.path.exists(filePath):
        pm.warning(f"The file {filePath} does not exist.")
        return

    with open(filePath, 'r') as json_file:
        data = json.load(json_file)

    return data