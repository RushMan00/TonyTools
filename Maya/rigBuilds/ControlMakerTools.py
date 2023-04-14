import maya.cmds as cmds
import pymel.core as pm

def scaleCurve(controlCurve = 'curve1',
               scale = 3):
    """
    to scale curve with out effecting int of scale
    ex. scale xyz will always be 1
    """
    spans = pm.getAttr( controlCurve+'.spans' )
    spanlist = pm.ls('curve1.cv[0:%s]'%spans, fl = True)
    pm.scale(scale,scale,scale, spanlist,a = True, ws = True)


def printVertPos(node=cmds.ls(sl=True)[0]):
    """
    When you create a shape manullly for curve controls
    this will spit out a list where the point are located in worldspace
    use cmds.curves and place the printed list in to the function
    """
    print('===== Copy =====')
    spans = mc.getAttr(node + '.spans')
    nbr = cmds.ls('curve1.cv[0:%s]' % spans, fl=True)
    print(nbr)
    for i in nbr:
        foo = cmds.pointPosition(i)
        print(str(tuple(foo)) + ',')
    print('===== End =====')
