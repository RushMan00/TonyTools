import pymel.core as pm
import json


def store_transform_data(filepath):
    """
    Store the translation and rotation values for selected objects in a JSON file

    Args:
        filepath (str): The filepath where the JSON file will be saved
    """

    # Get a list of all selected objects
    selected = pm.ls(selection=True)

    # Create an empty dictionary to store the values
    data = {}

    # Loop through each object and get its translate and rotate values
    for obj in selected:
        tx = obj.tx.get()
        ty = obj.ty.get()
        tz = obj.tz.get()
        rx = obj.rx.get()
        ry = obj.ry.get()
        rz = obj.rz.get()

        # Add the values to the dictionary
        data[obj.name()] = {
            "translate": [tx, ty, tz],
            "rotate": [rx, ry, rz]
        }

    # Write the dictionary to a JSON file
    with open(filepath, "w") as outfile:
        json.dump(data, outfile)

    # Print a confirmation message
    print("Transform data has been saved to '{}'".format(filepath))


def apply_transform_data(filepath):
    """
    Apply the translation and rotation values from a JSON file to objects in the scene

    Args:
        filepath (str): The filepath of the JSON file containing the transform data
    """
    # Load the transform data from the JSON file
    with open(filepath, "r") as infile:
        data = json.load(infile)

    # Set the transform values for each object based on its name
    for obj_name in data:
        obj = pm.PyNode(obj_name)  # Get the object by its name

        # Set the translation and rotation values
        obj.setTranslation(data[obj_name]["translate"])
        obj.setRotation(data[obj_name]["rotate"])

    # Print a confirmation message
    print("Transform data has been applied from '{}'".format(filepath))