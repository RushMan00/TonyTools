import maya.cmds as cmds
import pymel.core as pm
from rigBuilds import attribute

"""
this is to create anything invoing with the guides
"""

class locGuides():
    def __init__(self,
                 name='Base',
                 side='C',
                 size=1,
                 numberOfGuides=1,
                 color=1,
                 asChain=True,
                 mirror = False,
                 mirrorRotatoin = False,
                # # TODO
                #  upaxis:'y',
                # asChain:True,
                # parent:'C_joint1_JNT',
                 ):

        self.name = name
        self.side = side.upper()
        self.size = size
        self.numberOfGuides = numberOfGuides
        self.color = color
        self.asChain = asChain
        self.mirror = mirror
        self.mirrorRotatoin = mirrorRotatoin

        self.prefixName = 'GDE'
        self.tags = True
        #Vars
        self.mainGrp = None
        self.chainList = []
        self.locList = []
        self.guideList = []

        # self.__create()
        # initate
        self.__check()

    def __check(self):
        # check if a locator with the same name already exists in the scene
        loc_name = '{}_{}_'.format(self.side, self.name)
        for i in range(self.numberOfGuides):
            if pm.objExists(loc_name + str(i) + self.prefixName):
                pm.warning('A guide locator with the name {} already exists in the scene.'.format(
                    loc_name + str(i) + self.prefixName))
                return

        # if no duplicate locator names are found, create the main guide group
        self.mainGrp = pm.group(em=True, n='guide_{}_GRP'.format(self.name))
        self.chainList.append(self.mainGrp)
        self.__checkingSides()

    def __checkingSides(self):

        if self.side == 'C':
            self.side = 'C'
            if not self.color:
                self.color = 22
                self.__createStructure()
            if self.mirror:
                self.__createMirrorSetup()

        elif self.side == 'L':
            self.side = 'L'
            if not self.color:
                self.color = 4
                self.__createStructure()
            if self.mirror:
                self.__createMirrorSetup()

        elif self.side == 'R':
            self.side = 'R'
            if not self.color:
                self.color = 6
                self.__createStructure()
            if self.mirror:
                self.__createMirrorSetup()
        else:
            pm.warning('Please specify a "side".')
            return

    def __createStructure(self):
        locIter=[]
        # number of guides = number of structure
        for num in range(self.numberOfGuides):
            # crate locator
            name = self.side + '_' + self.name + str(num) + '_'
            mainLoc = pm.spaceLocator(n=name+self.prefixName)
            self.locList.append(mainLoc)
            locIter.append(mainLoc)
            pm.parent(mainLoc, self.chainList[-1])

            # --- set colour
            mainLocShape = mainLoc.getShape()
            mainLocShape.overrideEnabled.set(1)
            mainLocShape.overrideColor.set(self.color)

            # attach joint to locator as reference
            guideJnt = pm.joint(n=name+'JNT')
            guideJnt.template.set(True)
            pm.parent(guideJnt, mainLoc)

            if self.asChain:
                self.chainList.append(guideJnt)

            # create tags on locator and joints on locators
            if self.tags:
                pass
        # end of Loop

        # move locators for better selection in the world, more for UX in the scene
        for count, loc in enumerate(locIter):
            loc.translateBy([0, count, 0])

    def __createMirrorSetup(self):
        # Save the original side for later use
        originalSide = self.side
        # Determine the mirror side
        mirrorSide = 'L' if originalSide == 'R' else 'R'
        self.side = mirrorSide
        mirrorSide = 4 if originalSide == 'R' else 6
        self.color = mirrorSide

        # Create the mirrored structure
        self.__createStructure()

        # sort for L and right put it in different vars
        left = []
        right = []
        for word in self.locList:
            if "L" in word.name():
                left.append(word)
            elif "R" in word.name():
                right.append(word)

        # connect node from left to right XYZ mirrored
        for ct, (lft, rgt), in enumerate(zip(left, right)):
            pma = pm.createNode('plusMinusAverage', n=self.name + '_transform_Guides%s_PMA' % ct)
            lft.tx >> pma.input1D[0]
            lft.tx // pma.input1D[0]
            lft.tx >> pma.input1D[1]
            pma.operation.set(2)
            pma.input1D[0].set(0)
            pma.output1D >> rgt.tx
            # y and z
            lft.ty >> rgt.ty
            lft.tz >> rgt.tz

            if self.mirrorRotatoin:
                for i in ['rx', 'ry', 'rz']:
                    pma = pm.createNode('plusMinusAverage', n=self.name + '{}_Guides{}_PMA'.format(i,ct))
                    pma.operation.set(2)
                    pm.connectAttr(getattr(lft, i), pma.input1D[0], force=True)
                    pm.disconnectAttr(getattr(lft, i), pma.input1D[0])
                    pm.connectAttr(getattr(lft, i), pma.input1D[1], force=True)
                    pma.input1D[0].set(0)
                    pm.connectAttr(pma.output1D, getattr(rgt, i), force=True)
            else:
                lft.rx >> rgt.rx
                lft.ry >> rgt.ry
                lft.rz >> rgt.rz

        # tag locators
        for llst in self.locList:
            attribute.createTags(node=llst, tagName='locator', tagValue='LOC')






