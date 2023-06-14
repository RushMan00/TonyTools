import importlib as imp
import pymel.core as pm

from rigBuilds.rig import Joints, Tools
imp.reload(Joints)
imp.reload(Tools)

from rigBuilds import ControlCurves
imp.reload(ControlCurves)

class spline():
    def __init__(self,
                 side='C',
                 name='splineRig',
                 guideList=['C_spline%s_GDE' % i for i in range(5)],
                 numControls=4,
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
        self.fullName = '{}_{}'.format(side,name)
        self.iKhandle = None
        self.effector = None
        self.curveLength = int()
        self.jntList = []

        # initate
        self.__create()
        self.__cleanUp()

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
        # create joints evenly on curve and skin bind the joint controls
        controlJnts = Joints.addJointsAlongCurve(side=self.side,
                                                name=self.name +'Control',
                                                curve=self.curveName,
                                                numJoints=self.numControls, parent='RIG',
                                                tag=False, skinToCurve=True,
                                                primaryAxis='xyz',
                                                secondaryAxisOrient='yup')
        # create Curve controls
        for num, i in enumerate(controlJnts):
            ControlCurves.controlCurves(name=self.name,
                                         side=self.side,
                                         num=num,
                                         shape='square',
                                         rotate=[90, 0, 0],
                                         scale=3,
                                         parent = [i],
                                         parentOrConst='const',
                                         adjGrpNumber=1,
                                         hook = 'C_globalGimbal0_CNT',
                                         tag=True,
                                         )
        # create stretchy

    def __cleanUp(self):
        # remove locatorGuides Group
        par = pm.listRelatives(self.guideList[0], parent=True)
        pm.delete(par)




