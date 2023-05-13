import maya.cmds as cmds
import pymel.core as pm

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

def writeLocGuidesData(node='node', filePath = '\something'):
    # find the LocGuides in the scene
    locs = selectTaggedNodes(tagName=node)
    # read and store data in vars tx ty tz, rx ry rz
    for obj in locs:
        translation = obj.getTranslation()
        rotation = obj.getRotation()

        print(obj.name())
        print('translation', translation)
        print('rotation', rotation)

        return

    # store the data in to Jason file under the chosen paths
    return

def loadLocGuidesData(node='node', filePath = '\something'):
    # find the path of the data
    # find the LocGuides in the scene
    # load in the data with the names
    pass
