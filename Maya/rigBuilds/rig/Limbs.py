import importlib as imp
import pymel.core as pm
import maya.cmds as cmds
from rigBuilds import attribute
imp.reload(attribute)

from rigBuilds.rig import Joints, CurveTools, ControlCurves
imp.reload(Joints)
imp.reload(CurveTools)
imp.reload(ControlCurves)

class limbs():
    def __init__(self,
                 side='C',
                 name='arms',
                 guideList=['C_limbs%s_GDE' % i for i in range(3)],
                 addAttrsTo='C_global0_CNT',
                 FKcontrolColor=22,
                 IKcontrolColor=22,
                 FKcontrolSize=8,
                 IKcontrolSize=8,
                 parentJointsTo='C_chest_JNT',
                 primaryAxis='xyz',
                 secondaryAxisOrient='yup',
                 tagJoints=True,
                 # maybe
                 ):

        self.side = side
        self.name = name
        self.guideList = guideList
        self.jointList = [i.replace('_GDE', '_JNT') for i in self.guideList]
        self.addAttrsTo = addAttrsTo
        self.FKcontrolColor = FKcontrolColor
        self.IKcontrolColor = IKcontrolColor
        self.FKcontrolSize = FKcontrolSize
        self.IKcontrolSize = IKcontrolSize
        self.parentJointsTo = parentJointsTo
        self.primaryAxis = primaryAxis
        self.secondaryAxisOrient = secondaryAxisOrient
        self.tagJoints = tagJoints

        # Vars
        self.fullName = f'{side}_{name}'
        self.curveName = f'{side}_{name}_CRV'
        self.iKhandle = None
        self.effector = None
        self.curveLength = int()
        self.jntList = []
        self.crvAdjsGrp = None

        # initate
        self.__checker()
        self.__create()
        # self.__cleanUp()

    def __checker(self):
        # check if object exist by Names
        pass

    def __create(self):
        self.mainRigGroup = cmds.group(n=self.fullName + "limbRig_GRP", em=1, parent='RIG')
        mainLimbJoints = Joints.createJointChain(guideList=self.guideList,
                                                 parent=self.parentJointsTo,
                                                 primaryAxis='xyz',
                                                 orientJointEnd=True,
                                                 chain=True,
                                                 tag=self.tagJoints,
                                                 )

        IKLimbJoints = Joints.createJointChain(guideList=self.guideList,
                                               parent=self.parentJointsTo,
                                               primaryAxis='xyz',
                                               orientJointEnd=True,
                                               chain=True,
                                               tag=self.tagJoints,
                                               )
    def __cleanUp(self):
        # remove locatorGuides Group
        par = cmds.listRelatives(self.guideList[0], parent=True)
        cmds.delete(par)