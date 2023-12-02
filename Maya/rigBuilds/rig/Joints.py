import pymel.core as pm
import maya.cmds as cmds
import importlib as imp

from rigBuilds import attribute
imp.reload(attribute)

tagName = 'jointData'
tagValue = 'JNT'

"""
biped Orient Joints
chest       Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z
            
neck        Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z

head        Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z 
            End Joints fix - Joints rotate order xyz (eyes + head )
            
Left arm    Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z 
            End Joints fix - shoulder rotate order yxz - elbow rotate order yzx

thumb       thumb is rotated manully and iterate though joints with cmds.joint(e=1 zso = 1)

left hands  Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z 
            End Joints fix
            
left leg    Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z 
            End Joints fix - knees rotate order yzx
            
toes        Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Y 
            End Joints fix - Joints rotate order ZXY

all TWIST JOINTS rotate order ZXY
set perfered angels on root joint
"""

def tagAsJoints(object=[None]):
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
                attribute.createTags(nodeName=obj, attrName=tagName, attrValue=tagValue)
                taggedObjects.append(obj)
            else:
                print(f"Attribute {tagName} already exists on {obj}, skipping.")
        except Exception as e:
            print(f"Error tagging object {obj}: {e}")

    return taggedObjects

def selectTaggedJoints():
    ListofObject = attribute.selectTags(tagName=tagName)
    return ListofObject


def createJointChain(guideList=['C_spine%s_GDE' % i for i in range(5)],
                     parent='SKELE',
                     primaryAxis='xyz',
                     secondaryAxisOrient = 'yup',
                     orientJointEnd=True,
                     chain=True,
                     tag=True,
                     ):
    '''
    createJointChain() Function

    Creates a joint chain for rig setup.

    Usage:
    createJointChain(name='ACME', side='C', shape='acme', joints=['joint1'], scale=3,
    guideList=[], parent=None, primaryAxis='xyz', secondaryAxis='y', orientJointEnd=True, tag='')

    Parameters:
    - name (str): Name prefix for the joint chain.
    - side (str): Side identifier for the joint chain. Use 'L' for left, 'R' for right, 'C' for center.
    - shape (str): Shape identifier for the joint chain.
    - joints (list): Names of additional joints to be created in the chain.
    - scale (int): Scale factor for the joint chain.
    - guideList (list): Names of locGuides.
    - parent (str): Name of the parent joint to which the entire chain should be connected.
    - primaryAxis (str): Primary axis for joint orientation. Use 'x', 'y', or 'z'.
    - secondaryAxis (str): Axis that should point up for joint orientation.
    - orientJointEnd (bool): Flag indicating whether to orient the end joint of the chain with alignment.
    - tag (str): Tag for the current made joints.

    Returns:
    - list: List of joints as strings.

    Author: Tony K Song
    Date: 05/25/2023
    Version: 1.0.0
    '''

    jointList = []
    ChainedJntList = []
    ChainedJntList.append(parent)
    for guideNd in guideList:
        cmds.select(clear=True)
        # delete existing joint chain from scene
        jntName = guideNd.replace('_GDE', '_JNT')
        if cmds.objExists(jntName):
            cmds.delete(jntName)
        # create joints
        translation = cmds.getAttr(guideNd+".translate")[0]
        rotation = cmds.getAttr(guideNd+".rotate")[0]
        jnts = cmds.joint(
                         n=jntName,
                         p=translation,
                         o=rotation,
                         )
        cmds.select(jnts, d=True)
        jointList.append(jnts)
        if chain:
            # parent - create the joint chain
            cmds.parent(jnts, ChainedJntList[-1])
            ChainedJntList.append(jnts)
        else:
            cmds.parent(jnts, ChainedJntList)
        # tag
        if tag:
            tagAsJoints(object=[jnts])

    # Orient the joint chain
    cmds.select(jointList)
    cmds.joint(e=True, oj=primaryAxis,
               secondaryAxisOrient=secondaryAxisOrient,
               ch=True, zso=True)

    # Orient the end joint
    cmds.select(jointList[-1])
    cmds.joint(e=True, oj='none', ch=True, zso=orientJointEnd)
    cmds.select(jointList[-1], deselect=True)

    return jointList

def createJointsOnCurve(side='C',
                        name='JointControl',
                        curve='C_curve0_CRV',
                        numJoints=3, parent=None,
                        evenlyPlacedJoints=True,
                        tag=False, skinToCurve=True,
                        primaryAxis='xyz',
                        secondaryAxisOrient='yup',
                        ):
    """
    this tool to add joints evenly on a curve

    :param side:
    :param name:
    :param curve:
    :param numJoints:
    :param parent:
    :param tag:
    :param skinToCurve:
    :param primaryAxis:
    :param secondaryAxisOrient:
    :return:
    """

    # checks
    if numJoints < 3:
        cmds.warning('numJoints must be more than 3')

    fullname = '{}_{}'.format(side, name)
    grp = cmds.group(n=fullname + '_GRP')

    jointList = []

    for i in range(numJoints):
        # get curve points world location
        worldPositions = cmds.xform(f'{curve}.cv[{i}]', query=True,
                                    translation=True, worldSpace=True)

        # create joint on top of
        jnts = cmds.joint(n='{}_JNT'.format(fullname+str(i)),
                          p=worldPositions)
        cmds.setAttr(jnts + '.radius', 2)
        jointList.append(jnts)
        cmds.joint(jnts,
                   e=True, oj=primaryAxis,
                   secondaryAxisOrient=secondaryAxisOrient,
                   ch=True, zso=True)
        cmds.select(clear=1)

    jointList.pop(0)
    cmds.parent(jointList, grp)

    if parent:
        cmds.parent(grp, parent)

    if skinToCurve:
        skinCluster = cmds.skinCluster(jointList, curve,
                                       toSelectedBones=True, tsb=True, bm=0,
                                       dr=3, mi=1, lw=True, wt=0, omi=False)

    return jointList
