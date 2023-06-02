import pymel.core as pm

def createCurveOnPoints(name='C_curve0_CRV',
                        parent='RIG',
                        pointsOnNodes=[]
                        ):
    lst = []
    for point in pointsOnNodes:
        pnt = pm.PyNode(point)
        bah = pnt.translate.get()
        lst.append(bah)

    crv = pm.curve(n=name, p=lst)
    if parent:
        pm.parent(crv, parent)

    return lst
