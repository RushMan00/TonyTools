import pymel.core as pm
from rigBuilds import attribute
import importlib as imp

def createJointChain(guideList=['C_spine%s_GDE' % i for i in range(4)],
                     parent='SKELE',
                     primaryAxis='xyz',
                     secondaryAxisOrient = 'yup',
                     orientJointEnd=True,
                     tag=True,
                     ):
    '''
    FUNCTION:      createJointChain()
    DESCRIPTION:   Creates Joint Chains for rig setup
    USAGE:         createJointChain(name='ACME', side='C', shape='acme', joints=['joint1'], scale = 3,
    RETURN:        list of joint ex []
    AUTHOR:        Tony K Song
    DATE:          05/25/2023
    Version        1.0.0

    guideList       :   Names of locGuides
    parent          :   to parent the entire chain
    primaryAxis     :   xyz as default,
    secondayAxis    :   axis to point up to
    orientJointEnd  :   to orient the end joint of the chain with alignment the chain
    tag             :   to tag current made joints
    '''
    JntList = []
    otherJntList = []
    otherJntList.append(parent)
    jointList = []
    for guides in guideList:
        # delete existing chain from scene
        if pm.objExists(guides.replace('_GDE', '_JNT')):
            pm.delete(guides.replace('_GDE', '_JNT'))
        # create joints
        gde = pm.PyNode(guides)
        jnts = pm.joint(
                        n=guides.replace('_GDE', '_JNT'),
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