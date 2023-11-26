import maya.OpenMaya as OpenMaya
# WIP
class NodeControlCurve(object):
    def __init__(self, node_name, shape='circle'):
        self.node_name = node_name
        self.selection_list = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName(self.node_name, self.selection_list)
        self.dag_path = OpenMaya.MDagPath()
        self.selection_list.getDagPath(0, self.dag_path)
        self.curve_fn = OpenMaya.MFnNurbsCurve(self.dag_path)

        # Create the desired control shape
        if shape == 'circle':
            self.create_circle_shape()
        elif shape == 'square':
            self.create_square_shape()
        elif shape == 'triangle':
            self.create_triangle_shape()

    def create_circle_shape(self):
        # Create control vertices for a circle shape
        cvs = [(-1, 0, 0), (0, 1, 0), (1, 0, 0), (0, -1, 0), (-1, 0, 0)]

        # Set the control vertices of the curve
        self.curve_fn.setCVs(cvs)

        # Set the degree and knots of the curve
        self.curve_fn.setDegree(3)
        self.curve_fn.setKnots([0, 0, 0, 1, 2, 3, 4, 4, 4])

    def create_square_shape(self):
        # Create control vertices for a square shape
        cvs = [(-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)]

        # Set the control vertices of the curve
        self.curve_fn.setCVs(cvs)

        # Set the degree and knots of the curve
        self.curve_fn.setDegree(1)
        self.curve_fn.setKnots([0, 0, 1, 2, 3, 4, 4])

    def create_triangle_shape(self):
        # Create control vertices for a triangle shape
        cvs = [(0, 1, 0), (1, -1, 0), (-1, -1, 0), (0, 1, 0)]

        # Set the control vertices of the curve
        self.curve_fn.setCVs(cvs)

        # Set the degree and knots of the curve
        self.curve_fn.setDegree(1)
        self.curve_fn.setKnots([0, 0, 1, 2, 3, 3])

    def get_degree(self):
        return self.curve_fn.degree()

    def set_degree(self, degree):
        self.curve_fn.setDegree(degree)

    def get_knots(self):
        return self.curve_fn.knots

    def set_scale(self, scale):
        # Get the current scale of the curve
        current_scale = self.curve_fn.scale()

        # Set the new scale by multiplying the current scale by the input scale
        new_scale = OpenMaya.MVector(current_scale[0] * scale, current_scale[1] * scale, current_scale[2] * scale)
        self.curve_fn.setScale(new_scale)

