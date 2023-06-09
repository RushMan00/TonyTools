import pymel.core as pm
import importlib as imp

from rigBuilds import attribute
imp.reload(attribute)

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

def addJointsAlongCurve(side='C',
                        name='JointControl',
                        curve='C_curve0_CRV',
                        numJoints=3, parent=None,
                        tag=False, skinToCurve=True,
                        primaryAxis='xyz',
                        secondaryAxisOrient='yup',
                        ):
    fullname = '{}_{}'.format(side,name)

    if numJoints <3:
        pm.warning('numJoints must be more than 3')

    realCrv = pm.PyNode(curve)
    crvdup = pm.duplicate(curve)
    crv = pm.rename(crvdup, name+'DUP')
    # rebuild the curve with x amount of points with 1 Linear NOT 3Cubic
    rebldCrv = pm.rebuildCurve(crv, ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0,
                                kep=1, kt=0, s=numJoints+1, d=1, tol=0.01)
    pycrv = pm.PyNode(crv)
    jointList = [crv]

    for i in range(numJoints + 2):
        # get curve points world location
        worldPositions = pm.xform(pycrv.cv[i], query=True, translation=True, worldSpace=True)
        print(worldPositions)

        # create joint on top of
        jnts = pm.joint(n='{}_JNT'.format(fullname+str(i)),
                        p=worldPositions)
        jnts.radius.set(1.5)
        jointList.append(jnts.name())
        pm.joint(jnts,
                 e=True, oj=primaryAxis,
                 secondaryAxisOrient=secondaryAxisOrient,
                 ch=True, zso=True)
        pm.select(deselect=1)

    pm.delete(crv)
    jointList.pop(0)
    grp = pm.group(n=fullname+'_GRP')
    pm.parent(jointList, grp)
    # pm.parent(grp, jointList)

    if parent:
        pm.parent(grp,parent)

    if skinToCurve:
        skinCluster = pm.skinCluster(jointList, realCrv,
                                      toSelectedBones=True, tsb=True, bm=0,
                                      dr=3, mi=1, lw=True, wt=0, omi=False)

    return jointList