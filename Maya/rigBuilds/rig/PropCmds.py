import importlib as imp
import pymel.core as pm

from rigBuilds.rig import Joints
imp.reload(Joints)

from rigBuilds import ControlCurves
imp.reload(ControlCurves)

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
                 parentJointsGrpTo='SKELE',
                 jointChain=True,

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
        self.parentJointsGrpTo = parentJointsGrpTo
        self.jointChain = jointChain

        # Vars
        self.fullName = '{}_{}'.format(side, name)
        self.jntList = []

        # initiate
        self.__create()
        self.__cleanUp()

    def __create(self):
        # main group for the joints
        self.mainRigGroup = pm.group(n=self.fullName + "Joints_GRP", em=1,
                                     parent=self.parentJointsGrpTo)

        # create the joints
        self.jntList = Joints.createJointChain(guideList=self.guideList,
                                               parent=self.mainRigGroup,
                                               primaryAxis='xyz',
                                               orientJointEnd=True,
                                               chain=self.jointChain,
                                               tag=True,
                                               )

        # create Curve controls
        print(f'creating for {self.jntList}')
        for num, i in enumerate(self.jntList):
            ControlCurves.controlCurves(name=self.name,
                                        side=self.side,
                                        num=num,
                                        shape=self.shape,
                                        rotate=self.controlRotation,
                                        scale=self.controlSize,
                                        parent=[i],
                                        parentOrConst='const',
                                        adjGrpNumber=1,
                                        hook='C_god0_CNT',
                                        tag=True,
                                        )

    def __cleanUp(self):
        # # remove locatorGuides Group
        # par = pm.listRelatives(self.guideList[0], parent=True)
        # pm.delete(par)

        pass

