import pymel.core as pm
import attr
import importlib as imp

def createJointChain(guideList=['C_spline%s_GDE' % i for i in range(4)],
                     parent = None,
                     primaryAxis='xyz',
                     secondayAxis='z',
                     orientJointEnd=True,
                     tag=True,
                     ):
    '''
    FUNCTION:      createJointChain()
    DESCRIPTION:   Creates Joint Chains for rig setup
    USAGE:         createJointChain(name='ACME', side='C', shape='acme', joints=['joint1'], scale = 3,
    RETURN:        list of guides ex []
    AUTHOR:        Tony K Song
    DATE:          05/25/2023
    Version        1.0.0

    guideList       :   Names of locGuides
    parent          :   parent
    primaryAxis     :   xyz as default,
    secondayAxis    :   axis to point up to
    orientJointEnd  :   to orient the end joint of the chain with alignment the chain

    '''

    otherJntList = []
    otherJntList.append(parent)
    jointList = []
    # create joints
    for guides in guideList:
        gde = pm.PyNode(guides)
        jnts = pm.joint(n=guides,
                        p=gde.translate.get(),
                        o=gde.rotate.get(),
                        oj= primaryAxis,
                        sao=secondayAxis,
                        )
        jointList.append(jnts)
        # parent
        pm.parent(jnts,otherJntList[-1])
        # tag
        if tag:
            pass
        # orientJointEnd to last joint
        if orientJointEnd:
            pass

    return guideList