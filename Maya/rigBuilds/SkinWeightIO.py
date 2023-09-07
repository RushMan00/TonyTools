import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp
import xml.etree.ElementTree as ET

from rigBuilds import LoadMaFile, BaseRig, Checker, LocGuidesIO, LocGuides, attribute, ControlMakerTools
imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)
imp.reload(attribute)
imp.reload(ControlMakerTools)

tagName = 'skinweight'
tonyfilePath='D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'

def tagAsSkin(object=None):
    """
    Tag selected objects and objects from the input list as Skin str names.

    Args:
        input_list (list): List of objects to be tagged.

    Returns:
        list: A list containing the names of tagged objects.
    """
    # If input_list is not provided, default to an empty list
    if object is None:
        object = []
    # Create a copy of the input_list to prevent modifying the original list
    allObjects = object.copy()
    # Get currently selected objects in the Maya scene
    pm_objects = pm.ls(sl=1)
    # Add the names of selected objects to the allObjects list
    allObjects.extend(pm_obj.name() for pm_obj in pm_objects)
    # Print the names of all tagged objects
    for obj in allObjects:
        # Tag all objects as SKIN
        attribute.createTags(node=obj, tagName=tagName, tagValue='SKIN')
    # return list of tagged SkinWeights
    return allObjects

def selectTaggedSkins():
    """
    to only select objects that has tagged as "skin"
    :return: selected objects tag as "skin"
    """
    ListofObject = attribute.selectTags(tagName=tagName)
    return ListofObject

def exportTaggedSkinWeightMap(filePath='D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    # checking paths
    if not Checker.checkIfFilePathsExist(filePath):
        print('path is there continuing..')
        # go though each object and save out the skinweight data
        return

    for objectName in selectTaggedSkins():
        # Select the mesh with the skin cluster
        mesh = pm.PyNode(objectName)
        meshName = mesh.name()

        pm.deformerWeights(meshName+'.xml', path=filePath,
                           ex=True, sh=meshName, vc=True)

def importTaggedSkinWeightMap(filePath='D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    # look though the path and get the names of each file that has .xml exe store it

    # List all files in the directory
    fileDir = os.listdir(filePath)
    # Filter XML files and extract names without extensions
    xmlFilesNames = [file.split('.')[0] for file in fileDir if file.endswith('.xml')]
    # Print the extracted names
    for xmlFileName in xmlFilesNames:
        print(xmlFileName)

        # apply joints to mesh, get the source name in the xml file and appy all the joints as skinweight

        # List all files in the directory
        file_list = os.listdir(filePath)
        jointList=[]
        # Process each XML file
        for file in file_list:
            if file.endswith('.xml'):
                # print(file)
                # print(file)
                xml_path = os.path.join(filePath, file)
                # Parse the XML file
                tree = ET.parse(xml_path)
                root = tree.getroot()
                # Find elements with the 'source' attribute
                elements_with_source = root.findall(".//*[@source]")
                # Extract and print the 'source' attribute value
                for element in elements_with_source:
                    source_value = element.get('source')
                    jointList.append(source_value)
                    # print(f"File: {file}, Source: {source_value}")

                # must Create a skin cluster before applying data
                mesh = pm.PyNode(xmlFileName)
                skinCluster = None
                skinHis = pm.listHistory(mesh, type='skinCluster')

                # check if there is skin, store skinCluster
                if skinHis:
                    skinCluster = skinHis[0]  # Assuming there's only one skin cluster

                if skinCluster:
                    # Get the influence objects (joints) from the skin cluster
                    influences = skinCluster.getInfluence()
                    influence_names = [influence.name() for influence in influences]

                    # Compare influence_names and jointList, get remaining objects
                    remainingJoints = [item for item in jointList if item not in influence_names]

                    if remainingJoints:
                        # Add the remaining joints as influence objects
                        pm.skinCluster(skinCluster, edit=True, addInfluence=remainingJoints)

                # # fix this, some reason already has skin cluster
                # else:
                #     # Create a new skin cluster
                #     skinCluster = pm.skinCluster(jointList, mesh, toSelectedBones=True)[0]

                # get the list of names and then apply skinweight data from the xml
                pm.deformerWeights(xmlFileName + '.xml', path=filePath,
                                   im=True, sh=xmlFileName, vc=True)
                # # Tag Skinweights
                # tagAsSkin(object=xmlFileName)


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

# def OLDsaveSkinWeightsAsJson(filePath='D:/OneDrive/TonyTools/Maya/projects/pridapus/data'):
#     """
#     to only select objects that has tagged as "skin" will have their skinweight data saved
#     :return: selected objects tag as "skin"
#     """
#     # checking paths
#     if not Checker.checkIfFilePathsExist(filePath):
#         print('path is there continuing..')
#         # go though each object and save out the skinweight data
#         return
#
#     for objectName in selectTaggedSkins():
#         # Select the mesh with the skin cluster
#         mesh = pm.PyNode(objectName)
#
#         # Get the skin cluster
#         skin_cluster = None
#         for history_node in mesh.history():
#             if isinstance(history_node, pm.nt.SkinCluster):
#                 skin_cluster = history_node
#                 break
#         if not skin_cluster:
#             print(f"No skin cluster found on the selected mesh on {objectName}.")
#             continue
#
#         # Get skin weights
#         skin_weights = skin_cluster.getWeights(mesh)
#
#         # Create a dictionary to store skin weights
#         skin_data = []
#         influences = [joint.name() for joint in skin_cluster.influenceObjects()]
#         for vtx_index, vtx_weights in enumerate(skin_weights):
#             influence_indices = [influences.index(joint) for joint in influences]
#             skin_data.append({
#                 "vertexIndex": vtx_index,
#                 "influenceIndices": influence_indices,
#                 "weights": vtx_weights
#             })
#
#         # Create a dictionary for the output JSON format
#         output_dict = {
#             "sourceMesh": objectName,
#             "influences": influences,
#             "skinData": skin_data
#         }
#
#         # Save skin weights to a JSON file
#         jsonFilePath = os.path.join(filePath, f"{objectName}.json")
#         with open(jsonFilePath, 'w') as f:
#             json.dump(output_dict, f, indent=4)
#
#         print(f"Skin weights saved to {jsonFilePath}")