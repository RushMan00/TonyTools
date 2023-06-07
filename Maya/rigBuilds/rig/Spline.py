import importlib as imp
from rigBuilds.rig import Joints, Tools
imp.reload(Joints)
imp.reload(Tools)

import pymel.core as pm

class spline():
    def __init__(self,
                 side='C',
                 name='splineRig',
                 guideList=['C_spline%s_GDE' % i for i in range(5)],
                 numControls=2,
                 parentCurve='RIG',

                 hook = None,
                 # TODO sub controls
                 # subControl=False,
                 # subScale = [.8, .8, .8],
                 # subAdjGrpNumber=2,
                 ):


        self.side = side
        self.name = name
        self.guideList = guideList
        self.jointList = [i.replace('_GDE', '_JNT') for i in self.guideList]
        self.curveName = '{}_{}_CRV'.format(side,name)
        self.numControls = numControls
        self.parentCurve = parentCurve
        # Vars
        self.fullName= '{}_{}'.format(side,name)
        self.iKhandle = None
        self.effector = None
        self.curveLength = int()
        self.jntList = []

        # initate

        self.__create()

    def __create(self):
        self.mainRigGroup = pm.group(n=self.fullName + "_GRP", p='RIG')
        # create the joint chain
        spline = Joints.createJointChain(guideList=self.guideList,
                                         parent='SKELE',
                                         primaryAxis='xyz',
                                         orientJointEnd=True,
                                         tag=False,
                                         )
        # create the curve points on the joints
        crv = Tools.createCurveOnPoints(name=self.curveName, parent=self.parentCurve, nodeList=spline)
        crv = pm.PyNode(self.curveName)
        crv.setParent(self.mainRigGroup)
        # Create the IK Spline handle
        ikHandle = pm.ikHandle(n=self.fullName + 'iKHandle',
                               startJoint=self.jointList[0],
                               endEffector=self.jointList[-1],
                               solver="ikSplineSolver")
        self.iKhandle = ikHandle[0]
        self.effector = ikHandle[1]
        self.iKhandle.setParent(self.mainRigGroup)
        # Set the curve as the input curve for the IK Spline handle
        pm.ikHandle(self.iKhandle, e=True, curve=self.curveName)
        pm.delete(ikHandle[2])
        # create joints evenly base on arc length and number of controls pramater DO NOT need to tag
        Joints.addJointsAlongCurve(curve=self.curveName, numJoints=self.numControls, tag=False)

        # bind skin on joints to curve




