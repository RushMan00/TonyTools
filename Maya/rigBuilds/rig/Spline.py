import importlib as imp
import pymel.core as pm
import maya.cmds as cmds

from rigBuilds.rig import Joints, CurveTools, ControlCurves
imp.reload(Joints)
imp.reload(CurveTools)
imp.reload(ControlCurves)

class spline():
    def __init__(self,
                 side='C',
                 name='splineRig',
                 guideList=['C_spline%s_GDE' % i for i in range(5)],
                 numControls=4,
                 numberOfpointsOnIKCurve=5,
                 evenlyPlacedJoints=True,
                 parentCurve='RIG',

                 shape='circle',
                 controlColor=22,
                 controlSize=8,
                 controlRotation=[0, 0, 0],
                 parentJointsTo='monkeykingStickRoot_JNT',

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
        self.numberOfpointsOnIKCurve = numberOfpointsOnIKCurve
        self.numControls = numControls
        self.evenlyPlacedJoints = evenlyPlacedJoints,
        self.parentCurve = parentCurve

        self.shape = shape
        self.controlColor = controlColor
        self.controlSize = controlSize
        self.controlRotation = controlRotation
        self.parentJointsTo = parentJointsTo

        # Vars
        self.fullName = f'{side}_{name}'
        self.curveName = f'{side}_{name}_CRV'
        self.iKhandle = None
        self.effector = None
        self.curveLength = int()
        self.jntList = []

        # initate
        self.__create()
        self.__cleanUp()

    def __create(self):
        self.mainRigGroup = cmds.group(n=self.fullName + "_GRP", em=1)
        splineList = Joints.createJointChain(guideList=self.guideList,
                                             parent='SKELE',
                                             primaryAxis='xyz',
                                             orientJointEnd=True,
                                             tag=False,
                                             )

        # create the curve points on the joints
        crv = CurveTools.createCurveOnNodes(nodeList=splineList,
                                            name=self.curveName, parent=None,
                                            numberOfPoints=self.numberOfpointsOnIKCurve,
                                            degree=3, end=1)
        cmds.delete(crv, constructionHistory=1)
        cmds.parent(self.curveName, self.mainRigGroup)
        # Create the IK Spline handle
        ikHandle = cmds.ikHandle(n=self.fullName + 'iKHandle',
                                 startJoint=self.jointList[0],
                                 endEffector=self.jointList[-1],
                                 solver="ikSplineSolver", curve=self.curveName)

        self.iKhandle = ikHandle[0]
        self.effector = ikHandle[1]
        cmds.parent(self.iKhandle, self.mainRigGroup)
        # Set the curve as the input curve for the IK Spline handle
        controlJnts = Joints.createJointsOnCurve(side=self.side,
                                                 name=self.name + 'Control',
                                                 curve=self.curveName,
                                                 numJoints=self.numControls, parent='RIG',
                                                 tag=False, skinToCurve=True,
                                                 primaryAxis='xyz',
                                                 secondaryAxisOrient='yup')
        # # create Curve controls
        # for num, i in enumerate(controlJnts):
        #     ControlCurves.controlCurves(name=self.name,
        #                                 side=self.side,
        #                                 num=num,
        #                                 shape='square',
        #                                 rotate=[0, 0, 0],
        #                                 scale=self.controlSize,
        #                                 parent=[i],
        #                                 parentOrConst='const',
        #                                 adjGrpNumber=1,
        #                                 hook='C_god0_CNT',
        #                                 tag=True,
        #                                 )
        # create stretchy
        # x(y)= 5^3 = 1x1x1x1x1

    def __cleanUp(self):
        # remove locatorGuides Group
        par = cmds.listRelatives(self.guideList[0], parent=True)
        cmds.delete(par)




