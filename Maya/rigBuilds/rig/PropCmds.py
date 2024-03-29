import maya.cmds as cmds
import pymel.core as pm
import importlib as imp

from rigBuilds.rig import Joints, ControlCurves
imp.reload(Joints)
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
                 parentControlsTo=None,
                 parentJointsTo='SKELE',
                 lockHideAttrs=['sx', 'sy', 'sz'],
                 jointChain=True,
                 controlChain = True,
                 tagJoints=True,

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
        self.lockHideAttrs = lockHideAttrs
        self.jointChain = jointChain
        self.controlChain = controlChain
        self.tagJoints = tagJoints

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
        
        # #checking
        # # create the joints    # Fix in case of there is more that one of the same string in the list
        # # Loop through the original list
        # for string in self.guideList:
        #     # Add the string to the unique list if it's not already there
        #     if string not in self.guideList:
        #         self.guideList.append(string)
        
        print('____PropCmds____')
        print(self.guideList)
        print('____PropCmds____')
        
        self.jntList = Joints.createJointChain(side=self.side,
                                               name=self.name,
                                               guideList=self.jointList,
                                               parent=self.mainRigGroup,
                                               primaryAxis='xyz',
                                               orientJointEnd=True,
                                               chain=self.jointChain,
                                               tag=self.tagJoints,
                                               )
        # print('_+_+{+_+_+_+_+_}')
        # print(self.jntList)
        # print()
        self.controlList = ControlCurves.controlCurves(name=self.name,
                                                        side=self.side,
                                                        nodeList=self.jntList,
                                                        shape=self.shape,
                                                        rotate=self.controlRotation,
                                                        scale=self.controlSize,
                                                        parentOrConst='const',
                                                        adjGrpNumber=1,
                                                        controlChain=self.controlChain,
                                                        parentControlsTo=self.parentControlsTo,
                                                        lockHideAttrs=self.lockHideAttrs,
                                                        tag=True,
                                                        )

    def __cleanUp(self):
        # remove locatorGuides Group
        cmds.delete(cmds.listRelatives(self.guideList[0], parent=True))

    def getAllControlNames(self):
        return self.controlList

    # --- returns
    def __str__(self):
        return self.controlList[-1]

    # def __repr__(self):
    #     return self.finishedGrpLst[-1]

    # def getInstancesList(self):
    #     return self.finishedGrpLst
