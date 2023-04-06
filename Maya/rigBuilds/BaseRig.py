import maya.cmds as cmds
import pymel.core as pm
from rigBuilds import ControlCurves
reload(ControlCurves)

class baseRig():
    def __init__(self,
                 name='Base',
                 size=1,
                 children=['GEO','RIG','SKELE'],
                 nestingGrp={
                             'RIG' : ['C_main_GRP','C_global_GRP', 'C_globalBuffer_GRP','C_global_CTL', 'C_globalGimbal_CTL'],
                             'GEO' : ['C_main1_GRP', 'C_mainBuffer0_GRP' ],
                             'SKELE' : ['C_main2_GRP','C_mainBuffer2_GRP' ]
                             },

                # TODO
                #  colour: 1,
                #  upaxis:'y',
                 ):
        """

        :type children: list type
        """
        self.name = name
        self.size = size
        self.children = children
        self.nestingGrp = nestingGrp

        # TODO
        # self.colour = colour
        # self.upaxis = upaxis

        self.fullName = 'C_' + name + '_GRP'
        # procs
        self.__create()

    # def __instancecheck__(self, instance):

    def __createStructure(self):
        # create the main group
        mainGrp = pm.group(em=True, n=self.fullName)

        # create the child groups
        for stuff in self.children:
            grp = pm.group(em=True, n=stuff, p=mainGrp)

        # get values and make them in to groups
        for key, val in self.nestingGrp.items():
            bah = []
            num = 0
            for lst in val:
                if lst == val[0]:
                        pm.group(em=True, n=lst, p=key)
                        bah.append(lst)
                else:
                    if "CTL" in lst:
                        ControlCurves.controlCurves(name=lst,
                                                    side='C',
                                                    shape='acme',
                                                    rotate=[0, 0, 0],
                                                    scale=['1', '1', '1'],
                                                    joints=[],
                                                    parentConstTransform=False,
                                                    parentConstsetRotation=True,
                                                    adjGrpNumber=1,
                                                    )
                    else:
                        pm.group(em=True, n=lst, p=bah[num])
                        bah.append(lst)
                        num += 1

    # Exacute process
    def __create(self):
        # Step 1
        self.__createStructure()
        # self.__createGrpsandSubGrps()

