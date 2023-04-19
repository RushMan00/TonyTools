import maya.cmds as cmds
import pymel.core as pm
import logging

# Create a logger
_logger = logging.getLogger(__name__)

class controlCurves():
    def __init__(self,
                 name='ACME',
                 side='C',
                 shape='acme',
                 rotate=[0, 0, 0],
                 scale=['1', '1', '1'],
                 parent=['C_object01_JNT'],
                 parentOrConst='parent',
                 adjGrpNumber=2,
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
        setRotation     :   to set the Rotation base on joint rotation

        '''

        self.name = name
        self.side = side
        self.shape = shape
        self.scale = scale
        self.parents = parent
        self.parentOrConst = parentOrConst
        self.rotate = rotate
        self.adjGrpNumber = adjGrpNumber

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
        SUB GROUP       : C
        Controls        : CNT
        Constraint      : CONST
        """

        # Var
        # control Suffix Name
        self.CSN = "CNT"
        self.SUB = "SUB"
        # ex C_name0
        self.fullName = side + '_' + name
        # ex C_nameSub0
        self.subFullName =side + '_' + name + self.SUB
        # iteration of joints
        self.iterCounts = 0
        self.finalFullName = None
        self.controlNode = None
        self.controlNames = None
        self.grpLst = []
        self.innerCountShape = 0
        self.controlAndGrpLstNames = []
        self.crvShapeNames = []
        self.adjGrps = []
        # self.trans = pm.xform(self.joints, q=1, ws=1, rp=1)
        # self.rot = pm.xform(self.joints, q=1, ws=1, ro=1)

        # procs
        self.__create()

    def __initialSetup(self):
        for i in self.parents:
            # setup Var
            self.joint = i
            # self.iterCounts += 1
            self.finalFullName = self.side + '_' + self.name + str(self.iterCounts)

            if not cmds.objExists(self.finalFullName + '_' + self.CSN ):
                self.__createControl()
                self.iterCounts += 1
            else:
                logging.warning(self.finalFullName + "same name exists in scene.")
    # End of __initialSetup

    def __createControl(self):
        if self.shape == 'acme':  # Done
            self.acmeControl()
        elif self.shape == 'god':  # Done
            self.godControl()
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
                            " acme | pyramid | cube | god | square | arrowoutward | pinsquare | arrow")

    # ================================ THE CONTROL LIBRARY ================================
    # --- ACME CONTROL
    def acmeControl(self):
        self.innerCountShape = 0
        """ACME usually for things to put any attrs or pramas for over all rig """
        starcurve = pm.curve(name=self.finalFullName + "_star" + str(self.innerCountShape) + "_" + self.CSN,
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
        circleCurve = pm.circle(name=self.finalFullName + "_circle" + str(self.innerCountShape) + "_" + self.CSN,
                                nr=[0,180,0], ch = 0)[0]
        self.controlNames = pm.group(em=True, n=self.finalFullName + "_" + self.CSN)
        self.controlNode = pm.parent(starcurve.getShape(), circleCurve.getShape(), self.controlNames, s=True, r=True)
        pm.delete(starcurve, circleCurve)
    # End of ACME CONTROL

    # --- GOD CONTROL
    def godControl(self):
        crvNames = []
        rotateTo = 90
        for i in range(4):
            # create arrow curves
            arrowCrvName = pm.curve(name=self.finalFullName + "_GodArrow%s" % i + '_CNT', r=False, d=1,
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
            # create quarter of a circle
            circleCrvName = pm.curve(name=self.finalFullName + "_GodCircle%s" % i + '_CNT', r=False, d=1,
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
            arrowCrvName.setRotation([0, rotateTo * i, 0])
            circleCrvName.setRotation([0, rotateTo * i, 0])
            crvNames.append(arrowCrvName)
            crvNames.append(circleCrvName)

        # creating control grp and storing shape under group
        self.controlNames = pm.group(em=True, n=self.finalFullName + "_" + self.CSN)
        for i in crvNames:
            pm.makeIdentity(i, a=True, t=1, r=1, s=1, pn=1, n=0)
            self.controlNode = pm.parent(i.getShape(), self.controlNames, s=True, r=True)
            pm.delete(i)
    # END OF GOD CONTROL

    # --- Pyramid CONTROL
    def pyramidControl(self):
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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
        self.controlNames = pm.curve(name=self.finalFullName + "_" + self.CSN,
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

        name = self.finalFullName
        MainControlCrv = pm.PyNode(self.controlNames)

        # --- creating adj/buffer groups
        mainGrpName = pm.group(MainControlCrv, n=name + '_GRP')
        # self.adjGrps = []
        for i in range(self.adjGrpNumber):
            grp = pm.group(MainControlCrv, n=name+ "_" + 'Adj' + str(i) + '_GRP')
            self.adjGrps.append(grp)
        # find matrix of joints and set it on the frist dag group
        jnt = pm.PyNode(self.parents[0])
        jntMatrix = jnt.getMatrix()
        mainGrpName.setMatrix(jntMatrix)
        # END OF adj/buffer groups

        # TODO : make sub controls
        # --- creating sub adj/buffer groups
        # END OF sub adj/buffer groups

        if self.parentOrConst == 'parent' or 'Parent':
            pm.parent(MainControlCrv, self.parents[0])

        elif self.parentOrConst == 'const':
            bah = pm.parentConstraint(MainControlCrv, self.parents[0], mo=False, n=self.fullName+'Const')
            # End of  parent Constraints


        # --- move the shape of the controls
        for i in MainControlCrv.getShapes():
            a = str(i.getName())
            spans = pm.getAttr(i + '.spans')
            foo = pm.ls(i + '.cv[0:%s]' % spans, fl=True)
            """
            to scale curve without effecting int of scale attrs
            how it works: grab all the verties and scaling/rotating it togetehr
            """
            # cmds.setAttr(self.controlNames + '.t', self.trans[0], self.trans[1], self.trans[2])
            # cmds.setAttr(self.controlNames + '.r', self.rot[0], self.rot[1], self.rot[2])
            pm.scale(self.scale[0], self.scale[1], self.scale[2], foo, a=True, ws=True)
            pm.rotate(self.rotate[0], self.rotate[1], self.rotate[2], i + '.cv[0:%s]' % spans)

        # End of setting shape of controls

    def __return_objects(self):
        bah = self.controlNames
        return bah

    # Exacute process
    def __create(self):
        # Step 1
        self.__initialSetup()
        self.__createGrpsandSubGrps()
        self.__return_objects()
        # self.__controlAdj()
        # if self.subControl:
        #     self.__createSubControls()
