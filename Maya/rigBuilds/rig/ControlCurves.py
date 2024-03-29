import maya.cmds as cmds
import pymel.core as pm
import importlib as imp

from rigBuilds import attribute, Checker
imp.reload(attribute)
imp.reload(Checker)

class controlCurves():
    def __init__(self,
                 side='C',
                 name='ACME',
                 nodeList=['C_joint%s_JNT' % i for i in range(3)],
                 shape='acme',
                 scale=1,
                 color=None,
                 parentControlsTo=None,
                 parentOrConst='parent',
                 controlChain = False,
                 adjGrpNumber=2,
                 translate=[0, 0, 0],
                 rotate=[0, 0, 0],
                 lockHideAttrs = ['sx','sy','sz','v'],
                 tag = True,
                 subControl=False,
                 subScale = [.8, .8, .8],
                 subRotate=[0, 0, 0],
                 subAdjGrpNumber=2,
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
        self.nodeList = nodeList
        self.shape = shape
        self.scale = scale
        self.color = color
        self.controlChain = controlChain
        self.parentOrConst = parentOrConst
        self.parentControlsTo = parentControlsTo
        self.adjGrpNumber = adjGrpNumber
        self.translate = translate
        self.rotate = rotate
        self.lockHideAttrs = lockHideAttrs
        self.tag = tag
        self.subControl = subControl
        self.subScale = subScale
        self.subRotate = subRotate
        self.subAdjGrpNumber = subAdjGrpNumber

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
        # control Suffix Name
        self.CSN = "CNT"
        self.SUB = "SUB"

        # Var
        self.fullName = side + '_' + name  # ex C_name
        self.subFullName = side + '_' + name + self.SUB # ex C_nameSub
        self.mainFullName = self.side + '_' + self.name
        self.controlNode = None
        self.controlNames = None
        self.mainGrpList = []
        self.ControlList = []
        self.adjGrpList = []
        self.subaAdjGrpList =[]
        self.innerCountShape = 0
        self.controlAndGrpLstNames = []
        self.crvShapeNames = []
        self.adjGrps = []
        self.skipColor = 0
        # self.theList
        # self.trans = pm.xform(self.joints, q=1, ws=1, rp=1)
        # self.rot = pm.xform(self.joints, q=1, ws=1, ro=1)

        # Exacute process
        self.__checking()
        self.__creatingSetup()
        self.__cleanup()

    def __checking(self):
        # checking of any cotrol name is the same
        if Checker.checkIfObjectExist(objectList=[self.fullName + '_' + self.CSN]):
            print('please rename the control')
        # checking sides
        self.color = Checker.checkingSides(side=self.side, color=self.color)
        # making sure there is no double strings
        # uniqueNodes = []
        # for node in self.nodeList:
        #     # Add the string to the unique list if it's not already there
        #     if node not in uniqueNodes:
        #         self.nodeList.append(node)
        # # self.nodeList = uniqueNodes
        
        # print('__checking')
        # print("printing self.nodeList")
        # print(self.nodeList)
        # print('__checking_____________')

        
    def __chosingControls(self):
        if self.shape == 'acme':  # Done
            self.acmeControl()
        elif self.shape == 'circle':  # Done
            self.circleControl()
        elif self.shape == 'Hex':  # Done
            self.hexControl()
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
        elif self.shape == 'IKFK':  #
            self.IKFKswitchPannel()
        else:
            cmds.warning("wrong shape string. please chose one of the following in shapes: /n "
                         "circle | acme | pyramid | cube | god | square | arrowoutward | /n"
                         "pinsquare | arrow | IKFK")
    
            
    def mergingCurves(self, name='name', curveList = ['curve1', 'curve2']):
        "this tool is to create 1 core group for all shapes in the curveList"
        self.controlNames = cmds.group(em=True, n=name)
        for crvName in curveList:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in curveList:
            cmds.delete(crvName)
        return self.controlNames

    # ================================ THE CONTROL LIBRARY ================================
    # --- ACME CONTROL
    def acmeControl(self):
        self.innerCountShape = 0
        """ACME usually for things to put any attrs or pramas for over all rig """
        starcurve = cmds.curve(name=self.fullName + "_star" + str(self.innerCountShape) + "_" + self.CSN,
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
        cmds.rename(cmds.listRelatives(starcurve, shapes=True),
                    self.fullName + "_star" + str(self.innerCountShape) + "_" + self.CSN + 'Shape')
        circleCurve = cmds.circle(name=self.fullName + "_circle" + str(self.innerCountShape) + "_" + self.CSN,
                                nr=[0, 180, 0], ch = 0)[0]
        
        
        self.controlNames = cmds.group(em=True, n=self.fullName + "_" + self.CSN)
        self.controlNode = cmds.parent(starcurve.getShape(), circleCurve.getShape(), self.controlNames, s=True, r=True)
        cmds.delete(starcurve, circleCurve)
        
        crvNames=list()
        crvNames.append(starcurve)
        crvNames.append(circleCurve[0])

        self.controlNames = cmds.group(em=True, n=self.fullName + "_" + self.CSN)

        for crvName in crvNames:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in crvNames:
            cmds.delete(crvName)

        self.mergingCurves(name=self.fullName + "_" + self.CSN, 
                           curveList = [starcurve, circleCurve[0]])
    # End of ACME CONTROL
    
    # --- Circle CONTROL
    def circleControl(self):
        """circle control """
        self.controlNames = cmds.circle(name=self.fullName + "_" + self.CSN,
                                        nr=[0, 180, 0], r=1, s=8, ch=0)[0]
    # End of Circle CONTROL
    def globalControl(self):
        crvNames =[]
        self.innerCountShape = 0
        """global usually for base rig control"""
        tricurve = cmds.curve(name=self.fullName + "_triangle" + str(self.innerCountShape) + "_" + self.CSN,
                              r=False, d=1,  # k = True, a = True,
                              p=[
                                 (-0.6687143531977059, 0.0, 1.1278843667738405),
                                 (0.0, 0.0, 1.8020994704795177),
                                 (0.6687143531977059, 0.0, 1.1278843667738405),
                                 (-0.6687143531977059, 0.0, 1.1278843667738405),
                                ])
        shapes = cmds.listRelatives(tricurve, shapes=True)
        cmds.rename(shapes,
                    self.fullName + "_triangle" + str(self.innerCountShape) + "_" + self.CSN + 'Shape')
        circleCurve = cmds.circle(name=self.fullName + "_circle" + str(self.innerCountShape) + "_" + self.CSN,
                                  nr=[0, 180, 0], ch=0)
        crvNames.append(tricurve)
        crvNames.append(circleCurve[0])

        self.controlNames = cmds.group(em=True, n=self.fullName + "_" + self.CSN)

        for crvName in crvNames:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in crvNames:
            cmds.delete(crvName)
    # End of global CONTROL
    
    def HexControl(self):
        """Hex control """
        self.controlNames = cmds.circle(name=self.fullName + "_" + self.CSN,
                                        nr=[0, 180, 0], r=1, s=8, d=1, ch=0)
    # End of Hex CONTROL
    
    # --- GOD CONTROL
    def godControl(self):
        crvNames = []
        rotateTo = 90
        for nums in range(4):
            # create arrow curves
            arrowCrvName = cmds.curve(name=self.fullName + "_GodArrow" + str(nums) + '_CNT', r=False, d=1,
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
                        self.fullName + '_GodArrow' + str(nums) + "_" + self.CSN + 'Shape')
            cmds.setAttr(arrowCrvName + '.ry', rotateTo * nums)
            cmds.makeIdentity(arrowCrvName, apply=True, translate=True, rotate=True, scale=True)

            # create quarter of a circle
            circleCrvName = cmds.curve(name=self.fullName + '_GodCircle' + str(nums) + '_CNT', r=False, d=1,
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
                        self.fullName + "_GodCircle" + str(nums) + "_" + self.CSN + 'Shape')
            cmds.setAttr(circleCrvName + '.ry', rotateTo * nums)
            cmds.makeIdentity(circleCrvName, apply=True, translate=True, rotate=True, scale=True)

            crvNames.append(arrowCrvName)
            crvNames.append(circleCrvName)

        # creating control grp and storing shape under Curve group
        self.controlNames = cmds.group(em=True, n=self.fullName + "_" + self.CSN)
        for crvName in crvNames:
            shapes = cmds.listRelatives(crvName, shapes=True, fullPath=True) or []
            for shape in shapes:
                cmds.parent(shape, self.controlNames, shape=True, relative=True)
        for crvName in crvNames:
            cmds.delete(crvName)
    # END OF GOD CONTROL
    # --- Pyramid CONTROL
    def pyramidControl(self):
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
        self.controlNames = cmds.curve(name=self.fullName + "_" + self.CSN,
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
    
    def IKFKswitchPannel(self):
        I0 = cmds.curve(name=self.fullName+'I0_' + self.CSN,
                        r=False, d=1,  
                        p=[
                            (-0.703011848909553, 0.0, -0.21395467044878191),
                            (-0.8365544937196939, 0.0, -0.21395467044878191),
                            (-0.8365544937196939, 0.0, 0.217263705684129),
                            (-0.703011848909553, 0.0, 0.217263705684129),
                            (-0.703011848909553, 0.0, -0.21395467044878191),
                        ])
        cmds.rename(cmds.listRelatives(I0, shapes=True),
                    I0 + 'Shape')
        
        K0 = cmds.curve(name=self.fullName+'K0_' + self.CSN,
                        r=False, d=1,  
                        p=[
                        (-0.473071269679037, 0.0, -0.21395467044878191),
                        (-0.6063247665955872, 0.0, -0.21395467044878191),
                        (-0.6063247665955872, 0.0, 0.217263705684129),
                        (-0.473071269679037, 0.0, 0.217263705684129),
                        (-0.473071269679037, 0.0, 0.11204043198166103),
                        (-0.40422766332458343, 0.0, 0.03992572616746659),
                        (-0.3133116918788063, 0.0, 0.217263705684129),
                        (-0.14922068754315426, 0.0, 0.217263705684129),
                        (-0.31363696807062963, 0.0, -0.05118907242631954),
                        (-0.15628093466728238, 0.0, -0.21395467044878191),
                        (-0.3334985000240282, 0.0, -0.21395467044878191),
                        (-0.473071269679037, 0.0, -0.05099630041349634),
                        (-0.473071269679037, 0.0, -0.21395467044878191),

                        ])
        cmds.rename(cmds.listRelatives(K0, shapes=True),
                    K0 + 'Shape')
        
        F0 = cmds.curve(name=self.fullName+'F0_'+ self.CSN,
                        r=False, d=1,  
                        p=[
                        (0.39311178984504563, 0.0, -0.21395467044878191),
                        (0.06366488570983392, 0.0, -0.21395467044878191),
                        (0.06366488570983392, 0.0, 0.217263705684129),
                        (0.19750265254359817, 0.0, 0.217263705684129),
                        (0.19750265254359817, 0.0, 0.04107030872789885),
                        (0.36458161295236563, 0.0, 0.04107030872789885),
                        (0.36458161295236563, 0.0, -0.045996257345311986),
                        (0.19750265254359817, 0.0, -0.045996257345311986),
                        (0.19750265254359817, 0.0, -0.12129775650627495),
                        (0.39311178984504563, 0.0, -0.12129775650627495),
                        (0.39311178984504563, 0.0, -0.21395467044878191),
                        ])
        cmds.rename(cmds.listRelatives(F0, shapes=True),
                    F0 + 'Shape')
        
        K1 = cmds.curve(name=self.fullName+'K1_'+ self.CSN,
                        r=False, d=1,  
                        p=[
                            (0.6005341516221923, 0.0, -0.21395467044878191),
                            (0.46728067495693054, 0.0, -0.21395467044878191),
                            (0.46728067495693054, 0.0, 0.217263705684129),
                            (0.6005341516221923, 0.0, 0.217263705684129),
                            (0.6005341516221923, 0.0, 0.11204043198166103),
                            (0.6693778389817988, 0.0, 0.03992572616746659),
                            (0.760293810427576, 0.0, 0.217263705684129),
                            (0.9243848147632281, 0.0, 0.217263705684129),
                            (0.7599684937331761, 0.0, -0.05118907242631954),
                            (0.9173245676390998, 0.0, -0.21395467044878191),
                            (0.7401070022823542, 0.0, -0.21395467044878191),
                            (0.6005341516221923, 0.0, -0.05099630041349634),
                            (0.6005341516221923, 0.0, -0.21395467044878191),

                        ])
        cmds.rename(cmds.listRelatives(K1, shapes=True),
                    K1 + 'Shape')
        
        boarder = cmds.curve(name=self.fullName+'boarder0_'+ self.CSN,
                            r=False, d=1,  
                            p=[
                                (0.9945704879795692, 0.0, -0.49062999507472327),
                                (0.9945704879795692, 0.0, -0.49062999507472327),
                                (0.9945704879795692, 0.0, -0.49062999507472327),
                                (-0.9945704879795692, 0.0, -0.49062999507472327),
                                (-0.9945704879795692, 0.0, 0.5041904905847693),
                                (0.9945704879795692, 0.0, 0.5041904905847693),
                                (0.9945704879795692, 0.0, -0.49062999507472327),

                            ])
        cmds.rename(cmds.listRelatives(boarder, shapes=True),
                    boarder + 'Shape')
        
        self.controlNames = self.mergingCurves(name=self.fullName+'_'+self.CSN, curveList = [I0, K0, F0, K1, boarder])
        
        cmds.setAttr(boarder + 'Shape.overrideEnabled', 1)
        cmds.setAttr(boarder +'Shape.overrideColor', self.color)
        
        IKset = []
        FKset = []
        
        IKset.append(I0)
        IKset.append(K0)
        
        FKset.append(F0)
        FKset.append(K1)
        
        for ikLetters in IKset:
            cmds.setAttr(ikLetters + 'Shape.overrideEnabled', 1)
            cmds.setAttr(ikLetters  + 'Shape.overrideColor', 14)
            
        for fkLetters in FKset:
            cmds.setAttr(fkLetters + 'Shape.overrideEnabled', 1)
            cmds.setAttr(fkLetters  + 'Shape.overrideColor', 2)
        
        # setting up attrs
        attrSwitchName = attribute.addAttr(nodeName=self.controlNames, attrName='IKFKswitch', attributeType='float',
                                            min=0, max=1, defaultValue=0, enumName=None)

        # create FK condition nodes
        FKcondition = cmds.createNode('condition', n=f'{self.fullName}FK_condition')
        cmds.setAttr(FKcondition  + '.secondTerm', 1)
        cmds.setAttr(FKcondition  + '.colorIfTrueR', 14)
        cmds.setAttr(FKcondition  + '.colorIfFalseR', 2)
        cmds.connectAttr(attrSwitchName, FKcondition+'.firstTerm')
        for fkLetters in FKset:
            cmds.connectAttr(FKcondition+'.outColorR', fkLetters+'Shape.overrideColor')
            
        # create IK condition nodes
        IKcondition = cmds.createNode('condition', n=f'{self.fullName}IK_condition')
        cmds.setAttr(IKcondition  + '.secondTerm', 0)
        cmds.setAttr(IKcondition  + '.colorIfTrueR', 14)
        cmds.setAttr(IKcondition  + '.colorIfFalseR', 2)
        cmds.connectAttr(attrSwitchName, IKcondition+'.firstTerm')
        for ikLetters in IKset:
            cmds.connectAttr(IKcondition+'.outColorR', ikLetters+'Shape.overrideColor')
            
        self.skipColor = 1


    def __creatingSetup(self):
        # making controls for each iteration
        print('x.x.x.x.x.x.x.x')
        print(self.nodeList)
        for index, nodies in enumerate(self.nodeList):
            self.fullName = f'{self.fullName}{str(index)}'
             # creating controls
            self.__chosingControls()
            # creating main group
            mainControlName = cmds.group(self.controlNames, n=self.fullName + '_GRP')
            self.mainGrpList.append(mainControlName)
            # --- creating adj/buffer groups
            for i in range(self.adjGrpNumber):
                grp = cmds.group(self.controlNames, n=self.fullName + "_" + 'Adj' + str(i) + '_GRP')
                self.adjGrpList.append(grp)
            self.ControlList.append(self.controlNames)

            if self.subControl:
                for i in range(self.subAdjGrpNumber):
                    grp = cmds.group(self.controlNames, n=self.fullName + "_" + 'SubAdj' + str(i) + '_GRP')
                    self.adjGrpList.append(grp)
                self.ControlList.append(self.controlNames)
            print(nodies)
            matrix = cmds.xform(nodies, query=True, matrix=True, worldSpace=True)
            cmds.xform(mainControlName, matrix=matrix, worldSpace=True)
            # END OF adj/buffer groups
            
            if self.parentOrConst:
                if self.parentOrConst == 'parent':
                    if self.parentControlsTo == str():
                        cmds.parent(self.parentControlsTo, self.mainGrpList)

                elif self.parentOrConst == 'const':
                    cmds.parentConstraint(self.controlNames, nodies, mo=1,
                                          n=f'{self.fullName}_Const')
                    # End of  parent Constraints

            # set colour on locator shapes
            allShapes = attribute.getShapeNodes(nodeName=self.controlNames)
            if not self.skipColor:
                for ctlName in allShapes:
                    cmds.setAttr(ctlName + '.overrideEnabled', 1)
                    cmds.setAttr(ctlName + '.overrideColor', self.color)

            # --- move Shape Controls
            for ctlName in allShapes:
                # shapeName = ctlName + 'Shape'
                spans = cmds.getAttr(ctlName + '.spans')
                cmds.scale(self.scale, self.scale, self.scale, ctlName + '.cv[0:*]', r=True)
                cmds.rotate(self.rotate[0], self.rotate[1], self.rotate[2], ctlName + '.cv[0:*]')
                cmds.move(self.translate[0], self.translate[1], self.translate[2], ctlName + '.cv[0:*]', r =1)

            # --- self.tag
            if self.tag:
                attribute.createTags(nodeName=self.controlNames[0], attrName='type', attrValue='CNT')
            
            for lockHideAttr in self.lockHideAttrs:
                cmds.setAttr(f'{self.controlNames}.{lockHideAttr}', l=1, k=0, cb=0)

            self.fullName = self.fullName[:-1]
            
    def __cleanup(self):
        # --- parentControlsTo
        if self.parentControlsTo:
            if self.controlChain:
                # creating chain
                for control, group in zip(self.ControlList, self.mainGrpList[1:]):
                    cmds.parent(group, control)
                # parenting to
                cmds.parent(self.mainGrpList[0], self.parentControlsTo)
            else:
                cmds.parent(self.mainGrpList, self.parentControlsTo)

    # --- returns
    def __str__(self):
        return self.ControlList[-1]

    def __repr__(self):
        return self.ControlList[-1]

    def getControlName(self):
        return self.ControlList[-1]

    def geControlBase(self):
        return self.ControlList[0]

    def getInstancesList(self):
        return self.ControlList
# End of ControlCurve Class

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

def getPositionOfEachPointsOnCurve( node=   'cmds.ls(sl=True)[0]'   ):
                                    spans = cmds.getAttr(node + '.spans')
                                    nbr = cmds.ls(node+'.cv[0:%s]' %spans, fl=True)
                                    for i in nbr:
                                        foo = cmds.pointPosition(i)
                                        print(str(tuple(foo)) + ',')