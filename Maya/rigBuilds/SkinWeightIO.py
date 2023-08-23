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

def exportTaggedSkinWeightMap(filePath):
    # checking paths
    if not Checker.checkIfFilePathsExist(filePath):
        print('path is there continuing..')
        # go though each object and save out the skinweight data
        return

    for objectName in selectTaggedSkins():
        # Select the mesh with the skin cluster
        mesh = pm.PyNode(objectName)
        meshName = mesh.name()

        # Get the skin cluster
        skin_cluster = None
        for history_node in mesh.history():
            if isinstance(history_node, pm.nt.SkinCluster):
                skin_cluster = history_node
                break
        if not skin_cluster:
            print(f"No skin cluster found on the selected mesh on {objectName}.")
            continue

        pm.deformerWeights(meshName, ex=True, path=filePath)

def importTaggedSkinWeightMap(meshName, import_path):
    #look though the path

    #get all the names of files but remove.weightMap

    #
    weight_map = pm.PyNode(meshName)
    pm.deformerWeights(meshName, im=True, path=import_path)


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
#
# # Example usage:
# source_mesh = pm.PyNode("sourceMesh")
# target_meshes = [pm.PyNode("targetMesh1"), pm.PyNode("targetMesh2")]
# copySkinToo(source_mesh, target_meshes)

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
        skin_data = []
        influences = [joint.name() for joint in skin_cluster.influenceObjects()]
        for vtx_index, vtx_weights in enumerate(skin_weights):
            influence_indices = [influences.index(joint) for joint in influences]
            skin_data.append({
                "vertexIndex": vtx_index,
                "influenceIndices": influence_indices,
                "weights": vtx_weights
            })

        # Create a dictionary for the output JSON format
        output_dict = {
            "sourceMesh": objectName,
            "influences": influences,
            "skinData": skin_data
        }

        # Save skin weights to a JSON file
        jsonFilePath = os.path.join(filePath, f"{objectName}.json")
        with open(jsonFilePath, 'w') as f:
            json.dump(output_dict, f, indent=4)

        print(f"Skin weights saved to {jsonFilePath}")