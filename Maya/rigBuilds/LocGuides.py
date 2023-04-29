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
        self.side = side
        self.size = size
        self.numberOfGuides = numberOfGuides
        self.color = color
        self.asChain = asChain
        self.mirror = mirror
        self.mirrorRotatoin = mirrorRotatoin
        # # TODO
        # self.upaxis = upaxis
        # self.asChain = asChain
        # self.parent = parent

        self.prefixName = 'GDE'
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
        self.__createStructure()

    def __createStructure(self):

        for num in range(self.numberOfGuides):
            # crate locator
            name = self.side + '_' + self.name + '_' + str(num) + '_'
            mainLoc = pm.spaceLocator(n=name+'LOC')
            self.locList.append(mainLoc)
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
        # end of Loop

        # move locators for better visual selection
        for count, loc in enumerate(self.locList):
            loc.translateBy([0, count, 0])

            # if mirror - crate the mirror

            # if mirror rotation - mirror the rotation

            # if tags the guides and the joints




    def __create(self):
        self. __check()






