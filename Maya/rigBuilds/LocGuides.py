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
        self.tags=True
        #Vars
        self.mainGrp = None
        self.chainList = []
        self.locList = []

        self.__create()

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
        original_side = self.side
        # Determine the mirror side
        mirror_side = 'L' if original_side == 'R' else 'R'
        self.side = mirror_side
        color_side = 4 if original_side == 'R' else 6
        self.color = color_side

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

        # create node
        pma = pm.createNode('plusMinusAverage', n=self.name+'_transform_Guides'+'_PMA')
        # connect node from left to right XYZ mirrored
        # x

        for l, r, in zip(left, right):

            l.tx >> pma.input1D[0]
            l.tx // pma.input1D[0]
            l.tx >> pma.input1D[1]
            pma.operation.set(2)
            pma.input1D[0].set(0)
            pma.output1D >> r.tx
            # y and z
            l.ty >> r.ty
            l.tz >> r.tz

            if self.mirrorRotatoin:
                for i in ['rx', 'ry', 'rz']:
                    pma = pm.createNode('plusMinusAverage', n=self.name + '_' + i + '_Guides' + '_PMA')
                    pma.operation.set(2)
                    pm.connectAttr(getattr(l, i), pma.input1D[0], force=True)
                    pm.disconnectAttr(getattr(l, i), pma.input1D[0])
                    pm.connectAttr(getattr(l, i), pma.input1D[1], force=True)
                    pma.input1D[0].set(0)
                    pm.connectAttr(pma.output1D, getattr(r, i), force=True)

                else:
                    l.rx >> r.rx
                    l.ry >> r.ry
                    l.rz >> r.rz

            # if tags the guides and the joints

    def __create(self):
        self. __check()






