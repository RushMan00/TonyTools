import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp

from rigBuilds import LoadMaFile, BaseRig, Checker, LocGuidesIO, LocGuides, attribute, ControlMakerTools
imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)
imp.reload(attribute)
imp.reload(ControlMakerTools)

tagName = 'skinweight'

def selectTaggedSkins():
    """
    to only select objects that has tagged as "skin"
    :return: selected objects tag as "skin"
    """
    ListofObject = attribute.selectTags(tagName=tagName)
    return ListofObject


def saveSkinWeights(filePath='D:/OneDrive/TonyTools/Maya/projects/pridapus/data'):
    """
    to only select objects that has tagged as "skin" will have their skinweight data saved
    :return: selected objects tag as "skin"
    """
    # checking paths
    if not Checker.checkIfFilePathsExist(filePath):
        print('path is there continuing..')
        # go though each object and save out the skinweight data
        return

    for objectName in selectTaggedSkins():
        # Select the mesh with the skin cluster
        mesh = pm.PyNode(objectName)

        # Get the skin cluster
        skin_cluster = None
        for history_node in mesh.history():
            if isinstance(history_node, pm.nt.SkinCluster):
                skin_cluster = history_node
                break
        if not skin_cluster:
            print(f"No skin cluster found on the selected mesh on {objectName}.")
            continue

        # Get skin weights
        skin_weights = skin_cluster.getWeights(mesh)

        # Create a dictionary to store skin weights
        weights_dict = {}
        for vtx_index, vtx_weights in enumerate(skin_weights):
            joint_weights = {joint.name(): weight for joint, weight in
                             zip(skin_cluster.influenceObjects(), vtx_weights)}
            weights_dict[f"{objectName}.vtx[{vtx_index}]"] = joint_weights

        # Save skin weights to a JSON file
        jsonFilePath = os.path.join(filePath, f"{objectName}.json")
        with open(jsonFilePath, 'w') as f:
            json.dump(weights_dict, f, indent=4)

        print(f"Skin weights saved to {jsonFilePath}")

def LoadTaggedSkinWeights(filePath='\TonyTools\Maya\projects\pridapus\data'):
    """
    Load and apply skin weights from JSON files to objects tagged as "skin".
    """
    # Check if the specified directory exists
    if not os.path.exists(filePath):
        print(f"Directory {filePath} does not exist.")
        return

    # Iterate through each object and load skin weight data
    for objectName in selectTaggedSkins():  # Make sure selectTaggedSkins() returns object names
        # Select the mesh with the skin cluster
        mesh = pm.PyNode(objectName)

        # Get the skin cluster
        skin_cluster = None
        for history_node in mesh.history():
            if isinstance(history_node, pm.nt.SkinCluster):
                skin_cluster = history_node
                break
        if not skin_cluster:
            print(f"No skin cluster found on the selected mesh {objectName}.")
            continue

        # Load skin weights from the JSON file
        jsonFilePath = os.path.join(filePath, f"{objectName}.json")
        if not os.path.exists(jsonFilePath):
            print(f"JSON file {jsonFilePath} does not exist.")
            continue

        with open(jsonFilePath, 'r') as f:
            weights_dict = json.load(f)

        # Apply loaded skin weights
        for vtx_name, joint_weights in weights_dict.items():
            vtx_index = int(vtx_name.split('[')[1].split(']')[0])
            vtx = mesh.vtx[vtx_index]

            weights = [joint_weights.get(joint_name, 0.0) for joint_name in skin_cluster.influenceObjects()]
            skin_cluster.setWeights(vtx, weights)

        #reapply skinweight tag
        print(f"Skin weights loaded from {jsonFilePath} and applied to {objectName}")


def tagAsSkin(inputList=None):
    """
    Tag selected objects and objects from the input list as Skin str names.

    Args:
        input_list (list): List of objects to be tagged.

    Returns:
        list: A list containing the names of tagged objects.
    """
    # If input_list is not provided, default to an empty list
    if inputList is None:
        inputList = []
    # Create a copy of the input_list to prevent modifying the original list
    all_objects = inputList.copy()
    # Get currently selected objects in the Maya scene
    pm_objects = pm.ls(sl=1)
    # Add the names of selected objects to the all_objects list
    all_objects.extend(pm_obj.name() for pm_obj in pm_objects)
    # Print the names of all tagged objects
    for obj in all_objects:
        # Tag all objects as SKIN
        attribute.createTags(node=obj, tagName=tagName, tagValue='SKIN')
    # return list of tagged SkinWeights
    return all_objects

def copySkinToo():
    pass

