import pymel.core as pm
import importlib as imp

# from rigBuilds import attribute
# imp.reload(attribute)

def createJointChain(guideList=['C_spine%s_GDE' % i for i in range(5)],
                     parent='SKELE',
                     primaryAxis='xyz',
                     secondaryAxisOrient = 'yup',
                     orientJointEnd=True,
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

    JntList = []
    jointList = []
    otherJntList = []
    otherJntList.append(parent)

    for guideNd in guideList:
        # delete existing chain from scene
        jntName = guideNd.replace('_GDE', '_JNT')
        if pm.objExists(jntName):
            pm.delete(jntName)
        # create joints
        gde = pm.PyNode(guideNd)
        jnts = pm.joint(
                        n=jntName,
                        p=gde.translate.get(),
                        o=gde.rotate.get(),
                        )

        jointList.append(jnts)
        JntList.append(jnts)
        # parent - create the joint chian
        pm.parent(jnts, otherJntList[-1])
        otherJntList.append(jnts)
        # tag
        if tag:
            attribute.createTags(node=jnts, tagName='joint', tagValue='JNT')

    # Orient the joint chain
    pm.select(JntList)
    pm.joint(e=True, oj=primaryAxis,
             secondaryAxisOrient=secondaryAxisOrient,
             ch=True, zso=True)
    # Orient the end joint
    pm.select(JntList[-1])
    pm.joint(e=True, oj='none',ch=True, zso=orientJointEnd)
    pm.select(JntList[-1], deselect=True)

    return JntList