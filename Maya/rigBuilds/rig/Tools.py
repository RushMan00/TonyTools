import pymel.core as pm

import pymel.core as pm

def createCurveOnPoints(name='C_curve0_CRV', parent='RIG', nodeList=[]):
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

    lst = [pm.PyNode(point).getTranslation(space='world') for point in nodeList]

    crv = pm.curve(n=name, p=lst)

    if parent:
        crv.setParent(parent)

    return lst
