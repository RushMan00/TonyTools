
"""
this is to create anything invoing with the guides
"""

class guides():
    def __init__(self,
                 name='Base',
                 side='C',
                 size=1,
                 jointsNum: 1,
                 colour:1,
                 mirror: False,
                 mirrorRotatoin: False,
                # # TODO
                #  upaxis:'y',
                # asChain:True,
                # parent:'C_joint1_JNT',
                 ):

        self.name = name
        self.side = side
        self.size = size
        self.jointsNum = jointsNum
        self.colour = colour
        self.mirror = mirror
        self.mirrorRotatoin = mirrorRotatoin
        # # TODO
        # self.upaxis = upaxis
        # self.asChain = asChain
        # self.parent = parent
