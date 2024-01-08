import importlib as imp
import pymel.core as pm
import maya.cmds as cmds
from rigBuilds import attribute
imp.reload(attribute)

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
                 addAttrsTo='C_global0_CNT',
                 shape='circle',
                 controlColor=22,
                 controlSize=8,
                 controlRotation=[0, 0, 0],
                 parentJointsTo='monkeykingStickRoot_JNT',
                 primaryAxis='xyz',
                 secondaryAxisOrient='yup',
                 tagJoints=True,

                 hook = None,
                 ):

        self.side = side
        self.name = name
        self.guideList = guideList
        self.jointList = [i.replace('_GDE', '_JNT') for i in self.guideList]
        self.numberOfpointsOnIKCurve = numberOfpointsOnIKCurve
        self.numControls = numControls
        self.evenlyPlacedJoints = evenlyPlacedJoints,
        self.parentCurve = parentCurve
        self.addAttrsTo = addAttrsTo
        self.shape = shape
        self.controlColor = controlColor
        self.controlSize = controlSize
        self.controlRotation = controlRotation
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
        self.__create()
        self.__cleanUp()

    def __create(self):
        self.mainRigGroup = cmds.group(n=self.fullName + "SplineRig_GRP", em=1, parent='RIG')
        splineJointList = Joints.createJointChain(side=self.side,
                                                  name=self.name,
                                                  guideList=self.guideList,
                                                  parent=self.parentJointsTo,
                                                  primaryAxis='xyz',
                                                  orientJointEnd=True,
                                                  tag=self.tagJoints,
                                                  )
        ikHandle = cmds.ikHandle(name=self.fullName + 'iKHandle',
                                 startJoint=self.jointList[0],
                                 endEffector=self.jointList[-1],
                                 ccv=1, pcv=1,
                                 solver="ikSplineSolver",
                                #  parentCurve=self.mainRigGroup,
                                #  curve=self.curveName,
                                 numSpans=self.numberOfpointsOnIKCurve,
                                 )
        
        cmds.rename('curve1', self.curveName)
        cmds.parent(ikHandle[0], self.mainRigGroup)
        cmds.parent(ikHandle[1], self.mainRigGroup)
        cmds.parent(self.curveName, self.mainRigGroup)
        
        # Set the curve as the input curve for the IK Spline handle
        jointList = Joints.createJointsOnCurve(side=self.side,
                                                 name=self.name + 'Control',
                                                 curve=self.curveName,
                                                 numJoints=3, parent=self.mainRigGroup,
                                                 tagJoints=False, skinToCurve=True,
                                                 primaryAxis='xyz',
                                                 secondaryAxisOrient='yup')
        # create Curve controls
        mainControlList = ControlCurves.controlCurves(name=self.name,
                                                      side=self.side,
                                                      nodeList= jointList,
                                                      shape='square',
                                                      rotate=[0, 0, 0],
                                                      scale=self.controlSize,
                                                      parentOrConst='const',
                                                      adjGrpNumber=1,
                                                      controlChain=False,
                                                      parentControlsTo='C_cog0_CNT',
                                                      tag=True,
                                                      )
        # create stretchy setup
        # formula : x(y)= 5^3 = 1x1x1x1x1
        curveInfoNode = cmds.createNode('curveInfo', n=self.fullName+'Stretchy_curveInfo')
        cmds.connectAttr(self.curveName + '.worldSpace[0]', curveInfoNode + '.inputCurve')
        stretchyMuliDiv = cmds.createNode('multiplyDivide', n=self.fullName + 'Stretchy_multiplyDivide')
        cmds.setAttr(stretchyMuliDiv+".operation", 2)
        cmds.connectAttr(curveInfoNode+".arcLength", stretchyMuliDiv+'.input1X', f=1)
        arcLength = cmds.getAttr(curveInfoNode+'.arcLength')
        cmds.setAttr(stretchyMuliDiv+'.input2X', arcLength)
        for joint in splineJointList:
            axis = self.primaryAxis[0]
            cmds.connectAttr(stretchyMuliDiv + ".outputX", joint + f'.s{axis}', f=1)
        # adding attr setup to controls
        attribute.addAttrTitleSperator(nodeName=self.addAttrsTo, attrName='Stretchy')
        expoAttrs =[]
        attrExpoA = attribute.addAttr(nodeName=self.addAttrsTo, attrName='ExpoA',
                                      attributeType='float', min=0.0, max=10,
                                      defaultValue=1.25)
        expoAttrs.append(attrExpoA)

        attrExpoB = attribute.addAttr(nodeName=self.addAttrsTo, attrName='ExpoB',
                                      attributeType='float', min=0.0, max=10,
                                      defaultValue=1.5)
        expoAttrs.append(attrExpoB)

        attrExpoC = attribute.addAttr(nodeName=self.addAttrsTo, attrName='ExpoC',
                                      attributeType='float', min=0.0, max=10,
                                      defaultValue=1.25)
        expoAttrs.append(attrExpoC)

        squashMuliDiv = cmds.createNode('multiplyDivide', n=self.fullName + 'Squash_multiplyDivide')
        cmds.setAttr(squashMuliDiv + ".operation", 2)
        cmds.connectAttr(curveInfoNode + ".arcLength", squashMuliDiv + '.input2X', f=1)
        cmds.setAttr(squashMuliDiv + '.input1X', arcLength)
        expoStr=['ExpoA', 'ExpoB', 'ExpoC']
        for attr, str in zip(expoAttrs, expoStr):
            expo = cmds.createNode('multiplyDivide', n=f'{self.fullName}{str}_multiplyDivide')
            cmds.setAttr(expo + ".operation", 3)

            cmds.connectAttr(f'{attr}', expo + ".input1X", f=1)
            cmds.connectAttr(attr, expo + ".input1X", f=1)
            cmds.connectAttr(squashMuliDiv+".outputX", expo + ".input2X", f=1)

        cmds.connectAttr(self.fullName + expoStr[0] + "_multiplyDivide.outputX", self.jointList[1] + ".scaleY", f=1)
        cmds.connectAttr(self.fullName +expoStr[0] + "_multiplyDivide.outputX", self.jointList[1] + ".scaleZ", f=1)

        cmds.connectAttr(self.fullName +expoStr[1] + "_multiplyDivide.outputX", self.jointList[2] + ".scaleY", f=1)
        cmds.connectAttr(self.fullName +expoStr[1] + "_multiplyDivide.outputX", self.jointList[2] + ".scaleZ", f=1)

        cmds.connectAttr(self.fullName +expoStr[2] + "_multiplyDivide.outputX", self.jointList[3] + ".scaleY", f=1)
        cmds.connectAttr(self.fullName +expoStr[2] + "_multiplyDivide.outputX", self.jointList[3] + ".scaleZ", f=1)


    def __cleanUp(self):
        # remove locatorGuides Group
        par = cmds.listRelatives(self.guideList[0], parent=True)
        cmds.delete(par)




