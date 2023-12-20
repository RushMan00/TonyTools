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
        # must have 3 joints adviable

        pass

    def __create(self):
        """
        Notes: biped Orient Joints
        Left arm    Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z
                    End Joints fix - shoulder rotate order yxz - elbow rotate order yzx

        left leg    Primary Axis Y - Secondary Axis Z - Secondary Axis World Orientation Z
                    End Joints fix - knees rotate order yzx

        all TWIST JOINTS rotate order ZXY
        set perfered angels on root joint
        """

        self.mainRigGroup = cmds.group(n=self.fullName + "limbRig_GRP", em=1, parent='RIG')
        mainLimbJoints = Joints.createJointChain(side=self.side,
                                                 name=self.name+'Main',
                                                 guideList=self.guideList,
                                                 parent=self.parentJointsTo,
                                                 primaryAxis='yzx',
                                                 orientJointEnd=True,
                                                 chain=True,
                                                 deleteGuidesJoints=False,
                                                 tag=self.tagJoints,
                                                 )

        IKLimbJoints = Joints.createJointChain(side=self.side,
                                               name=self.name+'IK',
                                               guideList=self.guideList,
                                               parent=self.parentJointsTo,
                                               primaryAxis='yzx',
                                               orientJointEnd=True,
                                               chain=True,
                                               deleteGuidesJoints=False,
                                               tag=False,
                                               )

        FKLimbJoints = Joints.createJointChain(side=self.side,
                                               name=self.name+'FK',
                                               guideList=self.guideList,
                                               parent=self.parentJointsTo,
                                               primaryAxis='yzx',
                                               orientJointEnd=True,
                                               chain=True,
                                               deleteGuidesJoints=False,
                                               tag=False,
                                               )

        firstJointList = [mainLimbJoints[0], IKLimbJoints[0], FKLimbJoints[0]]
        secondJointList = [mainLimbJoints[1], IKLimbJoints[1], FKLimbJoints[1]]
        thirdJointList = [mainLimbJoints[2], IKLimbJoints[2], FKLimbJoints[2]]

        # setting rotate order for first Joint(arms)
        for firstJoint in firstJointList:
            cmds.setAttr(firstJoint+".rotateOrder", 4)
        # setting rotate order for second Joint(elbow)
        for secondJoint in secondJointList:
            cmds.setAttr(secondJoint+".rotateOrder", 1)

        # FK IK Setup
        cmds.parentConstraint(firstJointList[::-1], mo=1, w=1)
        cmds.parentConstraint(secondJointList[::-1], mo=1, w=1)
        cmds.parentConstraint(thirdJointList[::-1], mo=1, w=1)

        # creating controls for FK
        for num, i in enumerate(FKLimbJoints):
            ControlCurves.controlCurves(name=self.name,
                                        side=self.side,
                                        num=num,
                                        shape='circle',
                                        rotate=[0, 0, 0],
                                        scale=self.FKcontrolSize,
                                        parent=[i],
                                        parentOrConst='const',
                                        adjGrpNumber=1,
                                        hook='C_cog0_CNT',
                                        tag=True,
                                        )

    def __cleanUp(self):
        # # remove locatorGuides Group
        # par = cmds.listRelatives(self.guideList[0], parent=True)
        # cmds.delete(par)
        pass