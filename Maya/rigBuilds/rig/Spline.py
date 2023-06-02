import importlib as imp
from rigBuilds.rig import Joints
imp.reload(Joints)

import pymel.core as pm

class spline():
    def __init__(self,
                 side='C',
                 name='splineRig',
                 guideList=['C_spline%s_GDE' % i for i in range(4)],
                 numControls=2,

                 hook = None,
                 # TODO sub controls
                 # subControl=False,
                 # subScale = [.8, .8, .8],
                 # subAdjGrpNumber=2,
                 ):

        self.side = side
        self.name = name
        self.guideList = guideList
        self.numControls = numControls
        # Vars

        # initate
        self.__create()

    def __create(self):
        # create the joint chain
        spline = Joints.createJointChain(guideList=[self.guideList],
                                        parent='SKELE',
                                        primaryAxis='xyz',
                                        orientJointEnd=True,
                                        tag=True,
                                        )
        # create the curve points on the joints

        # create spline IK start to end then curves

        # create joints evenly base on arc length and number of controls pramater DO NOT need to tag

        # bind skin on joints

        pass


