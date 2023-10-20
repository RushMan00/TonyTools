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

        pm.deformerWeights(meshName+'.xml', path=filePath,
                           ex=True, sh=meshName, vc=True)

def importTaggedSkinWeightMap(filePath=r'D:\OneDrive\TonyTools\Maya\projects\pridapus\data\skinweights'):
    exist, modify_path = Checker.checkIfFilePathsExist(filePath)
    # List all files in the directory
    fileDir = os.listdir(modify_path)
    # Filter XML files and extract names without extensions
    xml_file_name = [file.split('.')[0] for file in fileDir if file.endswith('.xml')]
    # Print the extracted names
    for xml_file_name in xml_file_name:
        print(xml_file_name)
        # List all files in the directory
        file_list = os.listdir(filePath)
        jointList=[]
        # Processing each XML file
        for file in file_list:
            if file.endswith('.xml'):
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
                mesh = pm.PyNode(xml_file_name)
                skinCluster = None
                skinHis = pm.listHistory(mesh, type='skinCluster')
                print(skinHis)

                # check if there is skin, store skinCluster
                if skinHis:
                    skinCluster = skinHis[0]  # Assuming there's only one skin cluster
                    print('skincluster dose exist ' + skinCluster)

                    # if the skin cluster does exist
                    if skinCluster:
                        # Get the influenced objects (joints) from the skin cluster
                        influences = skinCluster.getInfluence()
                        influence_names = [influence.name() for influence in influences]
                        print(f'there is {influence_names} on {skinCluster}')
                        # Compare influence_names and jointList, get remaining objects
                        remainingJoints = [item for item in jointList if item not in influence_names]
                        print(f'the remaining Joints {remainingJoints}')
                        if not pm.objExists(remainingJoints):
                            # creating a dumpy one
                            for jnt in remainingJoints:
                                pm.joint(name=jnt)
                        pm.skinCluster(skinCluster, edit=True, weight=0, ai=remainingJoints)
                else:
                    # else create a new skin cluster wit the jointList
                    skinCluster = pm.skinCluster(jointList, mesh, toSelectedBones=True)[0]
                    # Tag Skinweights
                    tagAsSkin(object=xml_file_name)

                # get the list of names and then apply skinweight data from the xml
                pm.deformerWeights(xml_file_name + '.xml', path=filePath,
                                   im=True, sh=xml_file_name, vc=True)
                print('adding in existing xml skin data')


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
