import pymel.core as pm

# Create a function to create a locator at a given world position
def create_locator(name, world_pos):
    loc = pm.spaceLocator(name=name)
    loc.setTranslation(world_pos, space='world')
    return loc

# Get the selected objects
objects = pm.selected()

# Create a locator for each selected object
for obj in objects:
    name = obj.name() + "_LOC"
    world_pos = obj.getTranslation(space='world')
    create_locator(name, world_pos)

# Get the selected vertices and faces
verts = pm.ls(selection=True, fl=True, type='meshVertex')
faces = pm.ls(selection=True, fl=True, type='meshPolygon')

# Create a locator for each selected vertex
for vert in verts:
    name = vert.name() + "_LOC"
    world_pos = vert.getPosition(space='world')
    create_locator(name, world_pos)

# Create a locator for each selected face
for face in faces:
    name = face.name() + "_LOC"
    world_pos = face.getCenter(space='world')
    create_locator(name, world_pos)

# Get the selected points on curves
curves = pm.ls(selection=True, fl=True, type='nurbsCurve')
points = []
for curve in curves:
    points += curve.getCVs(space='world')

# Create a locator for each selected point on a curve
for point in points:
    name = curve.name() + "_LOC"
    create_locator(name, point)