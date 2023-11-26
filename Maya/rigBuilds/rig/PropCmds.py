import maya.cmds as cmds
import pymel.core as pm
import importlib as imp

from rigBuilds.rig import Joints
imp.reload(Joints)

class propCmds():
    def __init__(self,
                 side='C',
                 name='prop',
                 guideList=['C_prop%s_GDE' % i for i in range(5)],
                 shape='square',
                 controlColor=22,
                 controlSize=1,
                 controlRotation=[90, 0, 0],
                 parentControlsTo='C_god0_CNT',
                 parentJointsTo='SKELE',

                 jointChain=True,
                 controlChain = True,

                 # TODO sub controls
                 subControls = True,
                 subControlsColor = 22,
                 ):

        self.side = side
        self.name = name
        self.guideList = guideList
        self.jointList = [i.replace('_GDE', '_JNT') for i in self.guideList]
        self.shape = shape
        self.controlColor = controlColor
        self.controlSize = controlSize
        self.controlRotation = controlRotation
        self.parentControlsTo = parentControlsTo
        self.parentJointsTo = parentJointsTo
        self.jointChain = jointChain
        self.controlChain = controlChain

        # Vars
        self.fullName = '{}_{}'.format(side, name)
        self.jntList = []
        self.controlList = None

        # initiate
        self.__create()
        self.__cleanUp()

    def __create(self):
        # main group for the joints
        self.mainRigGroup = cmds.group(n=self.fullName + "Joints_GRP", em=1,
                                       parent=self.parentJointsTo)
        cmds.select(clear=True)

        # create the joints
        self.jntList = Joints.createJointChain(guideList=self.guideList,
                                               parent=self.mainRigGroup,
                                               primaryAxis='xyz',
                                               orientJointEnd=True,
                                               chain=self.jointChain,
                                               tag=True,
                                               )
        # Figure how to create control chain
        if self.controlChain:
            print(f'creating for control chain')
            hook = []
            hook.append(self.parentControlsTo)
            for num, parent in enumerate(self.jntList):
                self.controlList = ControlCurves.controlCurves(name=self.name,
                                                               side=self.side,
                                                               num=num,
                                                               shape=self.shape,
                                                               rotate=self.controlRotation,
                                                               scale=self.controlSize,
                                                               parent=parent,
                                                               parentOrConst='const',
                                                               adjGrpNumber=1,
                                                               hook=hook[-1],
                                                               tag=True,
                                                               )
                hook.append(self.controlList.getControlName())
                # self.controlList.getControlBase()

        else:
            # create Curve controls
            print(f'creating for {self.jntList}')
            for num, parent in enumerate(self.jntList):
                self.controlList = ControlCurves.controlCurves(name=self.name,
                                                              side=self.side,
                                                              num=num,
                                                              shape=self.shape,
                                                              rotate=self.controlRotation,
                                                              scale=self.controlSize,
                                                              parent=parent,
                                                              parentOrConst='const',
                                                              adjGrpNumber=1,
                                                              hook=self.parentControlsTo,
                                                              tag=True,
                                                              )

    def __cleanUp(self):
        # remove locatorGuides Group
        cmds.delete(cmds.listRelatives(self.guideList[0], parent=True))

    def getControlName(self):
        return self.controlList

    # --- returns
    def __str__(self):
        return self.controlList

    # def __repr__(self):
    #     return self.finishedGrpLst[-1]

    # def getInstancesList(self):
    #     return self.finishedGrpLst