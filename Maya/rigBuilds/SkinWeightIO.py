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
    # # check if paths exist
    # bools, paths = Checker.checkIfFilePathsExist(filePath)

    # Normalize and convert to an absolute path with forward slashes
    filePath = os.path.abspath(os.path.normpath(filePath)).replace('\\', '/')

    # Check if directory exists and is writable
    if not os.path.exists(filePath):
        print('Directory does not exist:', filePath)
        return
    if not os.access(filePath, os.W_OK):
        print('Directory is not writable:', filePath)
        return

    for objectName in selectTaggedSkins():
        if not cmds.objExists(objectName):
            print(f"{objectName} does not exist in the scene.")
            continue

        history = cmds.listHistory(objectName)
        skinClusters = [node for node in history if cmds.nodeType(node) == 'skinCluster']
        if not skinClusters:
            print(f"No skinCluster found on {objectName}")
            continue

        cmds.deformerWeights(objectName + '.xml', path=filePath,
                             ex=True, deformer=skinClusters[0], shape=objectName,  method='index')

        print('Export completed.')

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
        if not cmds.objExists(xml_file_name):
            print(f"The object {xml_file_name} does not exist in the scene.")
            continue

        mesh = pm.PyNode(xml_file_name)

        # Validate all joints exist
        for joint in joint_list:
            if not cmds.objExists(joint):
                print(f"The joint {joint} does not exist in the scene.")
                return

        # Find or create skin cluster
        skin_cluster = None
        skin_history = cmds.listHistory(mesh, type='skinCluster')

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
            attribute.createTags(nodeName=xml_file_name, attrName=tagName, attrValue=tagValue)
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
