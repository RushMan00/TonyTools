import maya.cmds as cmds
import pymel.core as pm
import importlib as imp

from rigBuilds import attribute
imp.reload(attribute)

import logging
_logger = logging.getLogger(__name__)

class controlCurves():
    def __init__(self,
                 side='C',
                 name='ACME',
                 num=0,
                 shape='acme',
                 rotate=[0, 0, 0],
                 scale=1,
                 color=None,
                 parent=None,
                 parentOrConst='parent',
                 adjGrpNumber=2,
                 hook = None,
                 tag = True,
                 # TODO sub controls
                 # subControl=False,
                 # subScale = [.8, .8, .8],
                 # subAdjGrpNumber=2,
                 ):
        '''
        FUNCTION:      ControlCurves.controlCurves()
        DESCRIPTION:   Creates Control Curves for animation
        USAGE:
                       CC.controlCurves(name='ACME', side='C', shape='acme', joints=['joint1'], scale = 3,
        RETURN:        ControlsCruves
        AUTHOR:        Tony K Song
        DATE:          02/07/21
        Version        beta 1.0.0

        Name            :   Name the main control
        side            :   Pass the sting like 'C' must be a sting and single or double letter
        shape           :   to set the shape of the object
        rotation        :   to set the Rotation base on joint rotation

        '''

        self.name = name
        self.side = side
        self.iterCounts = num
        self.shape = shape
        self.scale = scale
        self.color = color
        self.parent = parent
        self.parentOrConst = parentOrConst
        self.rotate = rotate
        self.adjGrpNumber = adjGrpNumber
        self.hook = hook
        self.tag = tag

        # TODO Create SubControls
        # self.subControl = subControl
        # self.subScale = subScale
        # self.subRotatePos = subRotatePos
        # self.subAdjGrpNumber = subAdjGrpNumber

        """
                RULES OF NAMING:
        when creating Cruve in maya curveShape1 is always named in crvShape, we haev to manually rename it
        == Naming Conventions ==

        SIDE
        Center  : CT
        left    : LT
        Right   : RT
        bottom  : BM
        Top     : TP
        back    : BK
        front   : FT

        Control iter name Example                        Example                         Discrpition
        Side_Discription01_TYPE                 :   C_object01_CNT              :   Control Name
        Side_Discription01_TYPEShape            :   C_Objects01_CNTShape        :   Control Shape Name
        Side_Discription01_buffer01_TYPE        :   C_Objects01_adj01_GRP       :   Controls adjustment group name

        GROUP           : GRP
        SUB GROUP       : SUB
        Controls        : CNT
        Constraint      : CONST
        joints          : JNT
        """

        # Var
        # control Suffix Name
        self.CSN = "CNT"
        self.SUB = "SUB"
        self.fullName = side + '_' + name  # ex C_name0
        self.subFullName =side + '_' + name + self.SUB # ex C_nameSub0
        self.finalFullName = self.side + '_' + self.name + str(self.iterCounts)
        self.controlNode = None
        self.controlNames = None
        self.finishedGrpLst = []
        self.innerCountShape = 0
        self.controlAndGrpLstNames = []
        self.crvShapeNames = []
        self.adjGrps = []
        # self.theList
        # self.trans = pm.xform(self.joints, q=1, ws=1, rp=1)
        # self.rot = pm.xform(self.joints, q=1, ws=1, ro=1)

        # procs
        self.__create()

    def __initialSetup(self):
        if not cmds.objExists(self.finalFullName + '_' + self.CSN ):
            self.__checkingSides()
            self.iterCounts += 1
        else:
            logging.warning(self.finalFullName + "same name exists in scene.")

    def __checkingSides(self):
        if self.side == 'C':
            self.side = 'C'
            if not self.color:
                self.color = 22
                self.__createControl()

        elif self.side == 'L':
            self.side = 'L'
            if not self.color:
                self.color = 4
                self.__createControl()

        elif self.side == 'R':
            self.side = 'R'
            if not self.color:
                self.color = 6
                self.__createControl()
        else:
            cmds.warning('Please specify a "side".')
            return
    # End of __initialSetup

    def __createControl(self):
        if self.shape == 'acme':  # Done
            self.acmeControl()
        elif self.shape == 'circle':  # Done
            self.circleControl()
        elif self.shape == 'god':  # Done
            self.godControl()
        elif self.shape == 'global':  # Done
            self.globalControl()
        # elif self.shape == 'godOffset':  # Done
        #     self.godControl()
        elif self.shape == 'pyramid':  # Done
            self.pyramidControl()
        elif self.shape == 'cube':  # Done
            self.cubeControl()
        elif self.shape == 'square':  # Done
            self.squareControl()
        elif self.shape == 'arrowoutward':  # Done
            self.arrowoutwardControl()
        elif self.shape == 'pinsquare':  # Done
            self.pinsquareControl()
        elif self.shape == 'arrow':  #
            self.arrowControl()
        else:
            logging.warning(" wrong shape string. please chose one of the following in shapes: /n "
                            "circle | acme | pyramid | cube | god | square | arrowoutward | pinsquare | arrow")

    # ================================ THE CONTROL LIBRARY ================================
    # --- ACME CONTROL
    # TODO FIXTHIS
    def acmeControl(self):
        self.innerCountShape = 0
        """ACME usually for things to put any attrs or pramas for over all rig """
        starcurve = cmds.curve(name=self.finalFullName + "_star" + str(self.innerCountShape) + "_" + self.CSN,
                             r=False, d=1,  # k = True, a = True,
                             p=[
                               (-2.2107888630062657e-16, 0.0, -0.9956507899629861),
                               (-0.24952876335791113, 0.0, -0.2792005778709363),
                               (-0.9706272589838668, 0.0, -0.23240215451241358),
                               (-0.29665382659753176, 0.0, 0.08216864315416685),
                               (-0.6115845176017596, 0.0, 0.7854009785356567),
                               (7.138106503438919e-17, 0.0, 0.3214717378901843),
                               (0.61158451760176, 0.0, 0.7854009785356565),
                               (0.29665382659753176, 0.0, 0.0821686431541667),
                               (0.9706272589838668, 0.0, -0.23240215451241403),
                               (0.24952876335791102, 0.0, -0.2792005778709364),
                               (-2.2107888630062657e-16, 0.0, -0.9956507899629861),
                           ])
        circleCurve = cmds.circle(name=self.finalFullName + "_circle" + str(self.innerCountShape) + "_" + self.CSN,
                                nr=[0, 180, 0], ch = 0)[0]
        self.controlNames = pm.group(em=True, n=self.finalFullName + "_" + self.CSN)
        self.controlNode = pm.parent(starcurve.getShape(), circleCurve.getShape(), self.controlNames, s=True, r=True)
        pm.delete(starcurve, circleCurve)
        self.controlNames = self.controlNames.name()
        print('A_A_A_A_A_A_A_A')
        print(self.controlNames)
    # End of ACME CONTROL

    # --- Circle CONTROL
    def circleControl(self):
        """circle control """
        self.controlNames = cmds.circle(name=self.finalFullName + "_" + self.CSN,
                                        nr=[0, 180, 0], r=1, s=8, ch=0)[0]

    def globalControl(self):
        crvNames =[]
        self.innerCountShape = 0
        """ACME usually for things to put any attrs or pramas for over all rig """
        tricurve = cmds.curve(name=self.finalFullName + "_triangle" + str(self.innerCountShape) + "_" + self.CSN,
                              r=False, d=1,  # k = True, a = True,
                              p=[
                                 (-0.6687143531977059, 0.0, 1.1278843667738405),
                                 (0.0, 0.0, 1.8020994704795177),
                                 (0.6687143531977059, 0.0, 1.1278843667738405),
                                 (-0.6687143531977059, 0.0, 1.1278843667738405),
                                ])
        shapes = cmds.listRelatives(tricurve, shapes=True)
        cmds.rename(shapes,
                    self.finalFullName + "_triangle" + str(self.innerCountShape) + "_" + self.CSN + 'Shape')
        circleCurve = cmds.circle(name=self.finalFullName + "_circle" + str(self.innerCountShape) + "_" + self.CSN,
                                  nr=[0, 180, 0], ch=0)
        crvNames.append(tricurve)
        crvNames.append(circleCurve[0])

        self.controlNames = cmds.group(em=True, n=self.finalFullName + "_" + self.CSN)

        for crvName in crvNames:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in crvNames:
            cmds.delete(crvName)
    # End of Circle CONTROL

    def HexControl(self):
        """Hex control """
        self.controlNames = cmds.circle(name=self.finalFullName + "_" + self.CSN,
                                        nr=[0, 180, 0], r=1, s=8, d=1, ch=0)
    # End of Circle CONTROL
    # --- GOD CONTROL
    def godControl(self):
        crvNames = []
        rotateTo = 90
        for nums in range(4):
            # create arrow curves
            arrowCrvName = cmds.curve(name=self.finalFullName + "_GodArrow" + str(nums) + '_CNT', r=False, d=1,
                                      # k = True, a = True,
                                      p=[
                                          (-0.24976468221459797, 0.0, -0.9990587288583922),
                                          (-0.24976468221459788, 0.0, -1.4985880932875884),
                                          (-0.49952936442919593, 0.0, -1.4985880932875884),
                                          (2.1411146302991436e-16, 0.0, -1.9981174577167844),
                                          (0.49952936442919627, 0.0, -1.4985880932875884),
                                          (0.24976468221459822, 0.0, -1.4985880932875884),
                                          (0.24976468221459813, 0.0, -0.9990587288583922),
                                      ])
            cmds.rename(cmds.listRelatives(arrowCrvName, shapes=True),
                        self.finalFullName + '_GodArrow' + str(nums) + "_" + self.CSN + 'Shape')
            cmds.setAttr(arrowCrvName + '.ry', rotateTo * nums)
            cmds.makeIdentity(arrowCrvName, apply=True, translate=True, rotate=True, scale=True)

            # create quarter of a circle
            circleCrvName = cmds.curve(name=self.finalFullName + '_GodCircle' + str(nums) + '_CNT', r=False, d=1,
                                       # k = True, a = True,
                                       p=[
                                           (-0.24976468221459794, 0.0, -0.9990587288583922),
                                           (-0.2965919365798677, 0.0, -0.9923691210919251),
                                           (-0.38934121742579897, 0.0, -0.9714072366081247),
                                           (-0.5214958437504207, 0.0, -0.9181227244860435),
                                           (-0.6434452788151456, 0.0, -0.8443475612891649),
                                           (-0.7519928599396136, 0.0, -0.7519928599396138),
                                           (-0.8443475612891649, 0.0, -0.6434452788151456),
                                           (-0.9181227244860434, 0.0, -0.5214958437504208),
                                           (-0.9714072366081238, 0.0, -0.38934121742579925),
                                           (-0.9923691210919247, 0.0, -0.296591936579868),
                                           (-0.9990587288583918, 0.0, -0.24976468221459822),
                                       ])
            cmds.rename(cmds.listRelatives(circleCrvName, shapes=True),
                        self.finalFullName + "_GodCircle" + str(nums) + "_" + self.CSN + 'Shape')
            cmds.setAttr(circleCrvName + '.ry', rotateTo * nums)
            cmds.makeIdentity(circleCrvName, apply=True, translate=True, rotate=True, scale=True)

            crvNames.append(arrowCrvName)
            crvNames.append(circleCrvName)

        # creating control grp and storing shape under Curve group
        self.controlNames = cmds.group(em=True, n=self.finalFullName + "_" + self.CSN)
        for crvName in crvNames:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in crvNames:
            cmds.delete(crvName)
    # END OF GOD CONTROL

    # --- Pyramid CONTROL
    def pyramidControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[(-0.7071066498756409, -0.5400000214576721, -0.70710688829422),
                                          (-0.7071068286895752, -0.5400000214576721, 0.7071067094802856),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (-0.7071066498756409, -0.5400000214576721, -0.70710688829422),
                                          (0.7071067690849304, -0.5400000214576721, -0.7071067690849304),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (0.7071067094802856, -0.5400000214576721, 0.7071068286895752),
                                          (0.7071067690849304, -0.5400000214576721, -0.7071067690849304),
                                          (0.0, 0.5400000214576721, 0.0),
                                          (-0.7071068286895752, -0.5400000214576721, 0.7071067094802856),
                                          (0.7071067094802856, -0.5400000214576721, 0.7071068286895752),
                                          ])
    # END of pyramidControl

    # --- CUBE CONTROL
    def cubeControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,*
                                       p=[
                                           (-0.5, 0.5, 0.5),
                                           (-0.5, 0.5, -0.5),
                                           (-0.5, -0.5, -0.5),
                                           (0.5, -0.5, -0.5),
                                           (0.5, 0.5, -0.5),
                                           (0.5, 0.5, 0.5),
                                           (0.5, -0.5, 0.5),
                                           (-0.5, -0.5, 0.5),
                                           (-0.5, 0.5, 0.5),
                                           (0.5, 0.5, 0.5),
                                           (0.5, -0.5, 0.5),
                                           (0.5, -0.5, -0.5),
                                           (0.5, 0.5, -0.5),
                                           (-0.5, 0.5, -0.5),
                                           (-0.5, -0.5, -0.5),
                                           (-0.5, -0.5, 0.5),
                                       ])
        # End of cubeControl

    # --- SQUARE CONTROL
    def squareControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                        (0.5, 1.1102230246251565e-16, -0.5),
                                        (0.5, -1.1102230246251565e-16, 0.5),
                                        (-0.5, -1.1102230246251565e-16, 0.5),
                                        (-0.5, 1.1102230246251565e-16, -0.5),
                                        (0.5, 1.1102230246251565e-16, -0.5),
                                         ])
    # END OF squareControl

    # --- arrowoutward Control
    def arrowoutwardControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                           (-0.5934552956583314, 0.0, 0.5934552956583314),
                                           (-0.19781843188611073, 0.0, 0.5934552956583314),
                                           (-0.19781843188611073, 0.0, 1.1869105913166629),
                                           (-0.5934552956583314, 0.0, 1.1869105913166629),
                                           (0.0, 0.0, 1.9781843188611032),
                                           (0.5934552956583314, 0.0, 1.1869105913166629),
                                           (0.19781843188611073, 0.0, 1.1869105913166629),
                                           (0.19781843188611073, 0.0, 0.5934552956583314),
                                           (0.5934552956583314, 0.0, 0.5934552956583314),
                                           (0.5934552956583314, 0.0, 0.19781843188611073),
                                           (1.1869105913166629, 0.0, 0.19781843188611073),
                                           (1.1869105913166629, 0.0, 0.5934552956583314),
                                           (1.9781843188611032, 0.0, 0.0),
                                           (1.1869105913166629, 0.0, -0.5934552956583314),
                                           (1.1869105913166629, 0.0, -0.19781843188611073),
                                           (0.5934552956583314, 0.0, -0.19781843188611073),
                                           (0.5934552956583314, 0.0, -0.5934552956583314),
                                           (0.19781843188611073, 0.0, -0.5934552956583314),
                                           (0.19781843188611073, 0.0, -1.1869105913166629),
                                           (0.5934552956583314, 0.0, -1.1869105913166629),
                                           (0.0, 0.0, -1.9781843188611032),
                                           (-0.5934552956583314, 0.0, -1.1869105913166629),
                                           (-0.19781843188611073, 0.0, -1.1869105913166629),
                                           (-0.19781843188611073, 0.0, -0.5934552956583314),
                                           (-0.5934552956583314, 0.0, -0.5934552956583314),
                                           (-0.5934552956583314, 0.0, -0.19781843188611073),
                                           (-1.1869105913166629, 0.0, -0.19781843188611073),
                                           (-1.1869105913166629, 0.0, -0.5934552956583314),
                                           (-1.9781843188611032, 0.0, 0.0),
                                           (-1.1869105913166629, 0.0, 0.5934552956583314),
                                           (-1.1869105913166629, 0.0, 0.19781843188611073),
                                           (-0.5934552956583314, 0.0, 0.19781843188611073),
                                           (-0.5934552956583314, 0.0, 0.5934552956583314),
                                       ])
    # END OF arrowoutward Control

    # --- pinsquare Control
    def pinsquareControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                           (0.0, 0.0, 0.0),
                                           (-1.0, 0.0, 0.0),
                                           (-1.0, 0.0, -2.0),
                                           (1.0, 0.0, -2.0),
                                           (1.0, 0.0, 0.0),
                                           (0.0, 0.0, 0.0),
                                           (0.0, 0.0, 4.0),
                                       ])
    # END OF pinsquareControl

    # --- arrow Control
    def arrowControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                            (-0.328797177570344, 0.0, 1.315188710281376),
                                            (0.328797177570344, 0.0, 1.315188710281376),
                                            (0.328797177570344, 0.0, 0.0),
                                            (0.986391532711032, 0.0, 0.0),
                                            (0.0, 0.0, -0.986391532711032),
                                            (-0.986391532711032, 0.0, 0.0),
                                            (-0.328797177570344, 0.0, 0.0),
                                            (-0.328797177570344, 0.0, 1.315188710281376),
                                            ])
    # End of arrowControl

    # --- triangle Control
    def triangleControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                          (-0.328797177570344, 0.0, 1.315188710281376),
                                          (0.328797177570344, 0.0, 1.315188710281376),
                                          (0.328797177570344, 0.0, 0.0),
                                          (0.986391532711032, 0.0, 0.0),
                                          (0.0, 0.0, -0.986391532711032),
                                          (-0.986391532711032, 0.0, 0.0),
                                          (-0.328797177570344, 0.0, 0.0),
                                          (-0.328797177570344, 0.0, 1.315188710281376),
                                         ])

    # End of triangleControl

    # --- star Control
    def starControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                           (-0.9956507899629861, 0.0, 0.0),
                                           (-0.27920057787093633, 0.0, 0.24952876335791108),
                                           (-0.2324021545124138, 0.0, 0.9706272589838668),
                                           (0.08216864315416678, 0.0, 0.29665382659753176),
                                           (0.7854009785356566, 0.0, 0.6115845176017598),
                                           (0.3214717378901843, 0.0, 0.0),
                                           (0.7854009785356566, 0.0, -0.6115845176017598),
                                           (0.08216864315416678, 0.0, -0.29665382659753176),
                                           (-0.2324021545124138, 0.0, -0.9706272589838668),
                                           (-0.27920057787093633, 0.0, -0.24952876335791108),
                                           (-0.9956507899629861, 0.0, 0.0),
                                       ])
    # End of starControl

    #--- gear Control
    def gearControl(self):
        self.controlNames = cmds.curve(name=self.finalFullName + "_" + self.CSN,
                                       r=False, d=1,  # k = True, a = True,
                                       p=[
                                           (-0.02792703607711131, 0.0, -1.009885145746707),
                                           (-1.9841134706071526e-08, 0.0, -0.8335609259098924),
                                           (0.25758447114099936, 0.0, -0.7927635909956867),
                                           (0.3386317963304868, 0.0, -0.9518280094926724),
                                           (0.5710021397035888, 0.0, -0.8334294618410324),
                                           (0.48995483935614026, 0.0, -0.6743650433440476),
                                           (0.6743650434252879, 0.0, -0.48995488895897676),
                                           (0.8334294122381959, 0.0, -0.571002238990503),
                                           (0.9518280592579903, 0.0, -0.3386318956174008),
                                           (0.7927636407610049, 0.0, -0.2575845455858748),
                                           (0.8335604788344357, 0.0, -2.9761702059107213e-08),
                                           (1.0098846986712504, 0.0, 0.027926970948000354),
                                           (0.9690874134411226, 0.0, 0.2855113346146863),
                                           (0.7927631439202305, 0.0, 0.2575843370102385),
                                           (0.674364596268591, 0.0, 0.4899545810151854),
                                           (0.8005987700864327, 0.0, 0.6161887548330273),
                                           (0.6161887647535942, 0.0, 0.8005988595340201),
                                           (0.4899545412516753, 0.0, 0.6743646360321011),
                                           (0.25758432208876714, 0.0, 0.7927631836837407),
                                           (0.28551134453525356, 0.0, 0.9690874035205551),
                                           (0.0279269870790774, 0.0, 1.0098847881188378),
                                           (-4.468317341724894e-08, 0.0, 0.8335605682820233),
                                           (-0.2575844362971526, 0.0, 0.7927632333678183),
                                           (-0.3386317863286785, 0.0, 0.951827651864803),
                                           (-0.5710020303336264, 0.0, 0.8334290545290864),
                                           (-0.48995468030209977, 0.0, 0.6743646857161786),
                                           (-0.6743647850030926, 0.0, 0.4899546306992629),
                                           (-0.8334291538160007, 0.0, 0.571001980730789),
                                           (-0.9518277014676398, 0.0, 0.3386317615678806),
                                           (-0.7927633823388097, 0.0, 0.2575843866943159),
                                           (-0.833560717253015, 0.0, -2.9761702059107213e-08),
                                           (-1.0098849370898295, 0.0, -0.027927024260894807),
                                           (-0.9690875524915468, 0.0, -0.28551144382216753),
                                           (-0.7927633823388097, 0.0, -0.25758444621772),
                                           (-0.67436483468717, 0.0, -0.4899547399067444),
                                           (-0.800599107873167, 0.0, -0.6161889137245863),
                                           (-0.6161890031721738, 0.0, -0.8005990681096566),
                                           (-0.4899547796702548, 0.0, -0.6743648942918147),
                                           (-0.25758451082326855, 0.0, -0.7927635413116094),
                                           (-0.28551153326975515, 0.0, -0.9690877611484243),
                                           (-0.02792703607711131, 0.0, -1.009885145746707),
                                       ])
    # End of gearControl

    def __createGrpsandSubGrps(self):
        # --- creating adj/buffer groups
        print(self.controlNames)
        mainGrpName = cmds.group(self.controlNames, n=self.finalFullName + '_GRP')
        self.finishedGrpLst.append(mainGrpName)
        for i in range(self.adjGrpNumber):
            grp = cmds.group(self.controlNames, n=self.finalFullName + "_" + 'Adj' + str(i) + '_GRP')
            self.finishedGrpLst.append(grp)
        self.finishedGrpLst.append(self.controlNames)

        # find matrix of parent and set it on the child
        if self.parent:
            matrix = cmds.xform(self.parent, query=True, matrix=True, worldSpace=True)
            cmds.xform(mainGrpName, matrix=matrix, worldSpace=True)
            # END OF adj/buffer groups
            if self.parentOrConst:
                if self.parentOrConst == 'parent':
                    cmds.parent(self.parent, self.controlNames)

                elif self.parentOrConst == 'const':
                    bah = cmds.parentConstraint(self.controlNames, self.parent, mo=False,
                                                n=f'{self.fullName}{str(self.iterCounts)}_Const')
                    # End of  parent Constraints
            else:
                pass

        # converting pymel to Sting because pymel node starts breaking here?
        allShapes = attribute.getShapeNodes(nodeName=self.controlNames)
        # set colour on locator shapes
        for ctlName in allShapes:
            cmds.setAttr(ctlName + '.overrideEnabled', 1)
            cmds.setAttr(ctlName + '.overrideColor', self.color)

        # TODO : make sub controls
        # --- creating sub adj/buffer groups
        # END OF sub adj/buffer groups

        # --- move position Shape Controls
        for ctlName in allShapes:
            # shapeName = ctlName + 'Shape'
            spans = cmds.getAttr(ctlName + '.spans')
            allSpans = cmds.ls(ctlName + '.cv[0:%s]' % spans, fl=True)

            # scaling the shape
            cmds.scale(self.scale, self.scale, self.scale, allSpans, r=True)
            # rotating the shape
            cmds.rotate(self.rotate[0], self.rotate[1], self.rotate[2], ctlName + '.cv[0:%s]' % len(allSpans))
        # --- self.hook
        if self.hook:
            # print('+_+_+_+_+_+_+_')
            # print(self.finishedGrpLst[0])
            cmds.parent(self.finishedGrpLst[0], self.hook)
        # --- self.tag
        if self.tag:
            attribute.createTags(nodeName=self.controlNames[0], attrName='type', attrValue='CNT')

    # --- returns
    def __str__(self):
        return self.finishedGrpLst[-1]

    def __repr__(self):
        return self.finishedGrpLst[-1]

    def getControlName(self):
        return self.finishedGrpLst[-1]

    def geControlBase(self):
        return self.finishedGrpLst[0]

    def getInstancesList(self):
        return self.finishedGrpLst

    # Exacute process
    def __create(self):
        # Steps
        self.__initialSetup()
        self.__createGrpsandSubGrps()

        # self.__return_objects()
        # self.__controlAdj()
        # if self.subControl:
        #     self.__createSubControls()


def scaleCurve(controlNames='C_global0_CNT', scale=1):
    """
    to scale curve with out effecting int of scale
    ex. scale xyz will always be 1
    """
    MainControlCrv = pm.PyNode(controlNames)
    for i in MainControlCrv.getShapes():
        a = str(i.getName())
        spans = pm.getAttr(i + '.spans')
        allSpans = cmds.ls(i + '.cv[0:%s]' % spans, fl=True)
        cmds.scale(scale, scale, scale, allSpans, r=True)