import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp
import xml.etree.ElementTree as ET

from rigBuilds import Checker, attribute
imp.reload(Checker)
imp.reload(attribute)

tagName = 'skinweight'
tagValue = 'skinweightData'
# tonyfilePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'

def tagAsSkin(object=[None]):
    """
    Tag objects as Skin. Objects can be provided as a list or selected in the Maya scene.
    Skips objects if the specified attribute already exists.

    Args:
        inputList (list, optional): List of objects to be tagged. Defaults to None.

    Returns:
        list: A list containing the names of successfully tagged objects.
    """
    if object is None:
        object = []

    # Optionally add currently selected objects in the Maya scene to the input list
    object.extend(cmds.ls(sl=1))

    taggedObjects = []
    for obj in object:
        try:
            # Check if the attribute already exists
            if not cmds.attributeQuery(tagValue, node=obj, exists=True):
                attribute.createTags(nodeName=obj, attrName=tagValue, attrValue=tagName)
                taggedObjects.append(obj)
            else:
                print(f"Attribute {tagName} already exists on {obj}, skipping.")
        except Exception as e:
            print(f"Error tagging object {obj}: {e}")

    return taggedObjects

def selectTaggedSkins():
    """
    to only select objects that has tagged as "skin"
    :return: selected objects tag as "skin"
    """
    ListofObject = attribute.selectTags(tagName=tagValue)
    return ListofObject

def exportTaggedSkinWeightMap(filePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    # check if paths exist
    bools, filePaths = Checker.checkIfFilePathsExist(filePath)

    for objectName in selectTaggedSkins():
        if not cmds.objExists(objectName):
            print(f"{objectName} does not exist in the scene.")
            continue

        history = cmds.listHistory(objectName)
        skinClusters = [node for node in history if cmds.nodeType(node) == 'skinCluster']
        if not skinClusters:
            print(f"No skinCluster found on {objectName}")
            continue

        cmds.deformerWeights(objectName + '.xml', path=filePaths,
                             ex=True, deformer=skinClusters[0], shape=objectName,  method='index')
        print('skinweight Export completed.')

def importTaggedSkinWeightMap(filePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    print('---- STARTING importing tagged Skin Weight Maps ----')
    exist, modifyPath = Checker.checkIfFilePathsExist(filePath)

    # List all XML files in the directory
    xmlFiles = [file for file in os.listdir(modifyPath) if file.endswith('.xml')]
    print(f'this is the list of files as xml {xmlFiles}')
    for xmlFile in xmlFiles:
        xmlFileName = xmlFile.split('.')[0]
        print(f"Going through {xmlFileName}")

        jointList = []
        skinList = []

        xmlPath = os.path.join(modifyPath, xmlFile)
        tree = ET.parse(xmlPath)
        root = tree.getroot()

        # Find elements with the 'source' attribute
        elementsWithSource = root.findall(".//*[@source]")
        for element in elementsWithSource:
            sourceValue = element.get('source')
            jointList.append(sourceValue)

        # Find elements with the 'deformer' attribute
        elementsWithDeformer = root.findall(".//*[@deformer]")
        for element in elementsWithDeformer:
            skinClusterName = element.get('deformer')
            skinList.append(skinClusterName)

        # Validate mesh exists
        if not cmds.objExists(xmlFileName):
            print(f"The object {xmlFileName} does not exist in the scene.")
            continue

        # Validate all joints exist
        for joint in jointList:
            if not cmds.objExists(joint):
                print(f"The joint {joint} does not exist in the scene.")
                return

        # Find or create skin cluster
        skinCluster = None
        # Filter for skinCluster nodes manually
        history = cmds.listHistory(xmlFileName)
        skinHistory = [node for node in history if cmds.nodeType(node) == 'skinCluster']

        # If there is a skin cluster, add in the joints that are not connected
        if skinHistory:
            skinCluster = skinHistory[0]  # Assuming there's only one skin cluster
            print(f'Skin cluster does exist: {skinCluster}')

            influences = cmds.skinCluster(skinCluster, query=True, inf=True)
            remainingJoints = [item for item in jointList if item not in influences]
            print(f'The remaining joints: {remainingJoints}')

            if remainingJoints:
                cmds.skinCluster(skinCluster, edit=True, weight=0, ai=remainingJoints)
        else:
            # Create new skin cluster
            skinCluster = cmds.skinCluster(jointList, xmlFileName, toSelectedBones=True, name=skinList[0])[0]
            print(f'Created new skin cluster: {skinCluster}')

        # Apply skin weights
        cmds.deformerWeights(xmlFile, im=True, path=modifyPath, method='index', deformer=skinCluster)
        print(f'Skin weights applied successfully with {xmlFile} data on {xmlFileName} with {skinCluster}.')

        for Files in xmlFiles:
            obj = Files.replace('.xml', '')
            print(obj)
            tagAsSkin([obj])

    print('---- FINISHED importing tagged Skin Weight Maps ----')


def copySkinToo(source_mesh, target_meshes):
    # Get the source mesh (with skin)
    source_skin_cluster = source_mesh.history(type='skinCluster')
    if not source_skin_cluster:
        pm.warning(f"No skin cluster found on {source_mesh}.")
        return
    source_skin_cluster = source_skin_cluster[0]
    influences = source_skin_cluster.getInfluence()

    # Get the skin weights data from the source skin cluster
    skin_weights = source_skin_cluster.getWeights(source_mesh)

    for target_mesh in target_meshes:
        # Get the vertices of the target mesh
        target_vertices = pm.ls(target_mesh + '.vtx[*]', flatten=True)

        # Apply the skin weights to the target mesh
        for i, vtx in enumerate(target_vertices):
            weights_to_apply = [skin_weights[i][influences.index(influence)] for influence in influences]
            source_skin_cluster.setWeights(target_mesh, vtx, influences, weights_to_apply)

    print("Skin weights copied successfully!")
