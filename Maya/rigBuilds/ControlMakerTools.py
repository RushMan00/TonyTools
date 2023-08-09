import maya.cmds as cmds
import pymel.core as pm


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


def printVertPos(node=cmds.ls(sl=True)[0]):
    """
    When you create a shape manullly for curve controls
    this will spit out a list where the point are located in worldspace
    use cmds.curves and place the printed list in to the function
    """
    print('===== Copy =====')
    spans = cmds.getAttr(node + '.spans')
    nbr = cmds.ls('curve1.cv[0:%s]' % spans, fl=True)
    print(nbr)
    for i in nbr:
        foo = cmds.pointPosition(i)
        print(str(tuple(foo)) + ',')
    print('===== End =====')
