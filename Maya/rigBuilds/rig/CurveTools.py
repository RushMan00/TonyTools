import maya.cmds as cmds
import pymel.core as pm

def createCurveOnNodes(nodeList=[], name='C_curve0_CRV',
                       parent='RIG', numberOfPoints=5,
                       degree=3, end=True,
                       ):
    '''
    createCurveFromNodes() Function

    Creates a curve from a list of node names.

    Args:
    - name (str): Name of the curve.
    - parent (str): Parent node under which the curve should be placed.
    - pointsOnNodes (list): List of node names to use for creating the curve points.

    Returns:
    - list: List of point translations.

    Author: Tony K Song
    Date: 06/05/2023
    Version: 1.0.0
    '''
    # checks
    if numberOfPoints < 3:
        cmds.warning('numberOfPoints must be more than 3')
        return

    # Create Curve
    lst = [cmds.xform(point, query=True, translation=True, worldSpace=True) for point in nodeList]
    crv = cmds.curve(n=name, p=lst)

    # Rename shapes
    shapes = cmds.listRelatives(crv, shapes=True)
    if shapes:
        cmds.rename(shapes[0], name + 'Shape')

    # Rebuild the curve
    rebild = cmds.rebuildCurve(name, ch=0, rpo=1, rt=0, end=end, kr=0,
                               kcp=0, kep=1, kt=0, s=numberOfPoints - 1,
                               d=degree, tol=0.01)



    # Parent the curve if a parent is specified
    if parent:
        cmds.parent(crv, parent)

    return crv
