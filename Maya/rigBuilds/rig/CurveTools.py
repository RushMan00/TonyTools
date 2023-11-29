import maya.cmds as cmds
import pymel.core as pm

def createCurveOnPoints(nodeList=[], name='C_curve0_CRV', parent='RIG'):
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

    # Get world space positions of the nodes and Create the curve
    lst = [cmds.xform(point, query=True, translation=True, worldSpace=True) for point in nodeList]
    crv = cmds.curve(n=name, p=lst)

    # Parent the curve if a parent is specified
    if parent:
        cmds.parent(crv, parent)

    return crv

