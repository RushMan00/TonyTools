import maya.cmds as cmds
import importlib as imp
import pymel.core as pm

from rigBuilds.rig import ControlCurves
imp.reload(ControlCurves)

# class baseRig():
#     def __init__(self,
#                  name='Base',
#                  size=1,
#                  groups={
#                          'RIG': ['C_main_GRP', 'C_global_CTL', 'C_globalGimbal_CTL', 'C_local_GRP'],
#                          'GEO': ['C_main1_GRP', 'C_mainBuffer0_GRP'],
#                          'SKELE': ['C_main2_GRP', 'C_mainBuffer2_GRP']
#                          },
#                 # TODO
#                 #  colour: 1,
#                 #  upaxis:'y',
#                  ):
#         """
#
#         :type children: list type
#         """
#         self.name = name
#         self.size = size
#         self.groups = groups
#
#         # TODO
#         # self.colour = colour
#         # self.upaxis = upaxis
#
#         self.fullName = 'C_' + name + '_GRP'
#         # procs
#         self.__create()
#
#     # def __instancecheck__(self, instance):
#     #     if pm.objExist(self.name):
#     #         logging.warning(self.finalFullName + "same name exists in scene.")
#
#     def __createStructure(self):
#         # create the main group
#         mainGrp = pm.group(em=True, n=self.name)
#         # create the child groups
#         for stuff in self.groups.keys():
#             grp = pm.group(em=True, n=stuff, p=mainGrp)
#
#         # get values and make them in to groups
#         for key, val in self.groups.items():
#             nextList = []
#             num = 0
#             for lst in val:
#                 if lst == val[0]:
#                     pm.group(em=True, n=lst, p=key)
#                     nextList.append(lst)
#                 else:
#                     if "CTL" in lst:
#                         val = lst.replace('C_', '').replace('_CTL', '')
#                         control = ControlCurves.controlCurves(name=val,
#                                                               side='C',
#                                                               shape='god',
#                                                               num=0,
#                                                               rotate=[0, 0, 0],
#                                                               scale=self.size - num,
#                                                               parent=[nextList[num]],
#                                                               parentOrConst='parent',
#                                                               hook=nextList[-1],
#                                                               adjGrpNumber=1,
#                                                               tag=True
#                                                               )
#                         print(control.getInstancesList()[-1])
#                         nextList.append(control.getInstancesList()[-1])
#                         num += 1
#                     else:
#                         bah = pm.group(em=True, n=lst, p=nextList[num])
#                         nextList.append(bah)
#                         num += 1
#
#     # Exacute process
#     def __create(self):
#         # Step 1
#         self.__createStructure()
#         # self.__createGrpsandSubGrps()

class baseRig2():
    def __init__(self,
                 name='Base',
                 size=1,
                 addRootJoint = True,

                 ):
        """
        QUICK WAY TO GET RIG BASE
        """
        self.name = name
        self.size = size
        self.addRootJoint = addRootJoint
        self.groups = ['GEO', 'RIG', 'SKELE']

        # TODO
        # self.colour = colour
        # self.upaxis = upaxis

        self.fullName = 'C_' + name + '_GRP'

        # Exacute process
        self.__createStructure()

    def __createStructure(self):
        # create the main group
        mainGrp = cmds.group(em=True, n=self.name)
        cmds.select(clear=1)
        # create the child groups
        for group in self.groups:
            grp = cmds.group(em=True, n=group, p=mainGrp)
            cmds.select(clear=1)
        main = cmds.group(em=True, n='C_main_GRP', p='RIG')
        cmds.select(clear=1)
        globalControl = ControlCurves.controlCurves(name='global',
                                                    side='C',
                                                    shape='global',
                                                    num=0,
                                                    rotate=[0, 0, 0],
                                                    scale=self.size,
                                                    hook = main,
                                                    # parent = ,
                                                    lockHideAttrs=['v'],
                                                    parentOrConst='parent',
                                                    adjGrpNumber=1,
                                                    tag=True
                                                    )

        godControl = ControlCurves.controlCurves(name='god',
                                                  side='C',
                                                  shape='god',
                                                  num=0,
                                                  rotate=[0, 0, 0],
                                                  scale= self.size / 2.2,
                                                  hook = globalControl,
                                                 lockHideAttrs=['v'],
                                                  parentOrConst='parent',
                                                  adjGrpNumber=1,
                                                  tag=True
                                                  )

        main = cmds.group(em=True, n='C_local_GRP', p=godControl)


        cmds.addAttr(globalControl.getControlName(),
                     shortName='gs', longName='globalScale',
                     defaultValue=1.0, minValue=0, k=1)

        for axis in 'xyz':
            cmds.connectAttr(f'{globalControl.getControlName()}.globalScale',
                             f'{globalControl.getControlName()}.s{axis}')

        if self.addRootJoint:
            cmds.select(clear=1)
            jnt = cmds.joint(n=f'root_JNT')
            cmds.parent(jnt, self.groups[-1])

            # connect to global scale
            for axis in 'xyz':
                cmds.connectAttr(f'{globalControl.getControlName()}.globalScale',
                                 f'{jnt}.s{axis}')
            # for rottran in 'tr':
            #     for axis in 'xyz':
            #         cmds.connectAttr(f'{globalControl.getControlName()}.{rottran}{axis}',
            #                          f'{jnt}.{rottran}{axis}')
            cmds.parentConstraint(godControl.getControlName(),
                                  jnt
                                  )
        # clean up