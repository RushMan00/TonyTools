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
            if pm.objExists(loc_name + str(i) + '_LOC'):
                pm.warning('A guide locator with the name {} already exists in the scene.'.format(
                    loc_name + str(i) + '_LOC'))
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
            mainLoc = pm.spaceLocator(n=name+'LOC')
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

            # if self.mirror:
            #     self.__createMirrorSetup()

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

        # # Calculate the mirrored positions
        # mirrored_positions = [pm.datatypes.Vector(-pos.x, pos.y, pos.z) for pos in original_positions]
        #
        # # Move the mirrored locators to the mirrored positions
        # for loc, pos in zip(self.locList[-len(mirrored_positions):], mirrored_positions):
        #     loc.setTranslation(pos, space='world')
        #
        # # Reset the side back to the original side
        # self.side = original_side

            # if mirror - crate the mirror

            # if mirror rotation - mirror the rotation

            # if tags the guides and the joints

    def __create(self):
        self. __check()






