import maya.cmds as cmds
import pymel.core as pm
import ControlNodes

class ribbon():
    def __init__(self,
                 side='C',
                 name='ribbon',
                 numjoints=6,
                 numControls=2,
                 startAxis = y,
                 backAxis = y,
                 hook = None,

                 # TODO sub controls
                 # subControl=False,
                 # subScale = [.8, .8, .8],
                 # subAdjGrpNumber=2,
                 ):

        self.name = name
        self.side = side
        self.numjoints = numjoints
        self.numControls = numControls
        self.startAxis = startAxis
        self.backAxis = backAxis
        # Vars

# REF
class Ribbon(object):
    def __init__(self, name, path_curve, num_controls, control_shape='circle'):
        self.name = name
        self.path_curve = path_curve
        self.num_controls = num_controls
        self.control_shape = control_shape

        # Create a group to hold the ribbon controls
        self.controls_grp = pm.group(empty=True, name='%s_controls_grp' % self.name)

        # Create a list to hold the control curves
        self.control_curves = []

        # Create control curves for each point on the path curve
        for i in range(self.num_controls):
            control_curve = ControlNodes.NodeControlCurve('%s_control_curve_%d' % (self.name, i), shape=self.control_shape)
            self.control_curves.append(control_curve)
            pm.parent(control_curve.node_name, self.controls_grp)

        # Create a group to hold the ribbon geometry
        self.geometry_grp = pm.group(empty=True, name='%s_geometry_grp' % self.name)

        # Create a NURBS surface to use as the ribbon geometry
        self.surface = pm.nurbsPlane(name='%s_surface' % self.name)

        # Set the degree of the ribbon surface to 1 in the U and V directions
        self.surface[0].setAttr('degreeU', 1)
        self.surface[0].setAttr('degreeV', 1)

        # Set the control points of the ribbon surface to match the positions of the control curves
        for i in range(self.num_controls):
            control_pos = pm.xform(self.control_curves[i].node_name, q=True, ws=True, t=True)
            self.surface[0].setAttr('controlPoints[%d][0]' % i, control_pos[0], control_pos[1], control_pos[2], 1.0)

        # Parent the ribbon surface to the ribbon geometry group
        pm.parent(self.surface[0], self.geometry_grp)

        # Create a curve to use as the path for the ribbon geometry
        self.path = pm.nurbsCurve(name='%s_path' % self.name, degree=1, p=self.path_curve[0].getCVs())

        # Attach the ribbon geometry to the path using a path constraint
        self.geometry_grp.setAttr('inheritsTransform', False)
        pm.pathAnimation(self.geometry_grp, self.path, fractionMode=True, follow=True, followAxis='x', upAxis='y')