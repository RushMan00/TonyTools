import maya.cmds as cmds
import pymel.core as pm
import json
import os
import importlib as imp
import xml.etree.ElementTree as ET

from rigBuilds import BaseRig, Checker, attribute
imp.reload(BaseRig)
imp.reload(Checker)
imp.reload(attribute)

tagName = 'skinweight'
tagValue = 'SKIN'
tonyfilePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'

def tagAsSkin(object=[None]):
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
        attribute.createTags(node=obj, tagName=tagName, tagValue=tagValue)
    # return list of tagged SkinWeights
    return allObjects

def selectTaggedSkins():
    """
    to only select objects that has tagged as "skin"
    :return: selected objects tag as "skin"
    """
    ListofObject = attribute.selectTags(tagName=tagName)
    return ListofObject

def exportTaggedSkinWeightMap(filePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    # checking paths
    if not Checker.checkIfFilePathsExist(filePath):
        print('path is there continuing..')
        # go though each object and save out the skinweight data
        return

    for objectName in selectTaggedSkins():
        # Select the mesh with the skin cluster
        mesh = pm.PyNode(objectName)
        meshName = mesh.name()

        # List the history of the geometry and find the skinCluster
        history = pm.listHistory(meshName)
        skinClusters = [node for node in history if isinstance(node, pm.nodetypes.SkinCluster)]
        if not skinClusters:
            print(f"No skinCluster found on {meshName}")
        print(f'there is {skinClusters[0].name()} on {meshName}')

        # get skincluster name from geo
        pm.deformerWeights(meshName+'.xml', path=filePath, df=skinClusters[0].name(),
                           ex=True, sh=meshName, vc=True)


def importTaggedSkinWeightMap(filePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    print('---- STARTING importing tagged Skin Weight Maps ----')
    exist, modify_path = Checker.checkIfFilePathsExist(filePath)
    if not exist:
        print(f"The specified file path does not exist.")
        return

    # List all XML files in the directory
    xml_files = [file for file in os.listdir(modify_path) if file.endswith('.xml')]
    print(f'this is the list of files as xml {xml_files}')
    for xml_file in xml_files:
        xml_file_name = xml_file.split('.')[0]
        print(f" going though {xml_file_name}")

        joint_list = []
        skin_list = []

        xml_path = os.path.join(modify_path, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find elements with the 'source' attribute
        elements_with_source = root.findall(".//*[@source]")
        for element in elements_with_source:
            source_value = element.get('source')
            joint_list.append(source_value)

        # Find elements with the 'deformer' attribute
        elements_with_deformer = root.findall(".//*[@deformer]")
        for element in elements_with_deformer:
            skin_cluster_name = element.get('deformer')
            skin_list.append(skin_cluster_name)

        # Validate mesh exists
        if not pm.objExists(xml_file_name):
            print(f"The object {xml_file_name} does not exist in the scene.")
            continue

        mesh = pm.PyNode(xml_file_name)

        # Validate all joints exist
        for joint in joint_list:
            if not pm.objExists(joint):
                print(f"The joint {joint} does not exist in the scene.")
                return

        # Find or create skin cluster
        skin_cluster = None
        skin_history = pm.listHistory(mesh, type='skinCluster')

        # if there is skin cluster add in the joints that are not connected
        if skin_history:
            skin_cluster = skin_history[0]  # Assuming there's only one skin cluster
            print(f'Skin cluster does exist: {skin_cluster.name()}')

            influences = skin_cluster.getInfluence()
            influence_names = [influence.name() for influence in influences]
            print(f'There are {influence_names} on {skin_cluster.name()}')

            remaining_joints = [item for item in joint_list if item not in influence_names]
            print(f'The remaining joints: {remaining_joints}')

            # if remaining_joints:
            pm.skinCluster(skin_cluster, edit=True, weight=0, ai=remaining_joints)
        # else add in the skin cluster relative to the xml file
        else:
            # if there is more than one skincluster might have to change it here
            skin_cluster = pm.skinCluster(joint_list, mesh, toSelectedBones=True, name=skin_list[0])
            print(f'Created new skin cluster: {skin_cluster}')

        # Apply skin weights
        pm.deformerWeights(xml_file, path=modify_path, im=True, method='index', deformer=skin_cluster)
        print(f'Skin weights applied successfully with {xml_file} data on {xml_file_name} with {skin_cluster}.')
        if not attribute.checkAttributeExists(xml_file_name, tagName):
            attribute.createTags(node=xml_file_name, tagName=tagName, tagValue=tagValue)
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
