import os
import shutil
import maya.cmds as cmds


class AssetCreator():
    def __init__(self,
                 paths=r"D:/OneDrive/TonyTools/Maya/projects"):

        self.paths = paths
        self.createAssetWindow = None
        self.assetPathTextField = None
        self.createUiWindow()

    def create_asset_folder(self, *args):
        assetPath = cmds.textField(self.assetPathTextField, query=True, text=True)

        "find the modeling file of the asset, make sure to Check that path ends with .ma or .mb"
        if not assetPath.endswith(".ma") and not assetPath.endswith(".mb"):
            cmds.warning("Please make sure the Asset Path ends with .ma or .mb")
            return

        # Check if the file exists
        if not os.path.exists(assetPath):
            cmds.warning("The file does not exist at the provided path.")
            return

        asset_name = os.path.splitext(os.path.basename(assetPath))[0]
        asset_folder_path = os.path.join(self.paths, asset_name)

        # Check if the asset folder already exists
        if os.path.exists(asset_folder_path):
            cmds.warning(f"The asset folder '{asset_name}' already exists. Please choose a different asset name.")
            return

        # Create the asset folder
        os.makedirs(asset_folder_path)
        print("Created asset folder:", asset_name)

        # Create the data and model folders
        data_folder_path = os.path.join(asset_folder_path, "data")
        model_folder_path = os.path.join(asset_folder_path, "model")
        os.makedirs(data_folder_path)
        os.makedirs(model_folder_path)

        # Create the Python file based on the asset file
        python_file_name = f"{asset_name}.py"
        python_file_path = os.path.join(asset_folder_path, python_file_name)
        with open(python_file_path, "w") as python_file:
            python_file.write(projectTemp)

        # Create the locGuides and skinweights folders under data folder
        loc_guides_folder_path = os.path.join(data_folder_path, "locGuides")
        skin_weights_folder_path = os.path.join(data_folder_path, "skinweights")
        os.makedirs(loc_guides_folder_path)
        os.makedirs(skin_weights_folder_path)

        # Copy asset file to the model folder
        modelAssetPath = os.path.join(model_folder_path, os.path.basename(assetPath))
        shutil.copy(assetPath, modelAssetPath)
        print("Sucssecful, Copied asset file to the model folder.")

        # make this work!
        # UI.riggingUI.refreshAssetList()
        return

    def createUiWindow(self):
        if cmds.window("CreateNewAssetWindow", exists=True):
            cmds.deleteUI("CreateNewAssetWindow", window=True)

        self.createAssetWindow = cmds.window("CreateNewAssetWindow", title="Create New Asset", widthHeight=(300, 120))
        create_asset_layout = cmds.columnLayout(adjustableColumn=True)

        cmds.text(label=" find the modeling file of the asset")
        cmds.text(label="copy and paste the path and include the file with extenstion (with .ma or .mb extension):")
        cmds.text(label= r'for example : C:\Users\kimoo\OneDrive\Desktop\cube.ma')
        self.assetPathTextField = cmds.textField()
        cmds.button(label="Create the Asset Structure", command=self.create_asset_folder)
        cmds.text(label=r'This will add a name in the rigging UI Asset list, base on the file name')
        cmds.setParent('..')
        cmds.showWindow(self.createAssetWindow)

projectTemp = """import pymel.core as pm
import maya.cmds as cmds
import importlib as imp

# rigbuilds modules
from rigBuilds import LocGuides, attribute
imp.reload(LocGuides)
imp.reload(attribute)

# rig modules
from rigBuilds.rig import PropCmds, ControlCurves
imp.reload(PropCmds)
imp.reload(ControlCurves)

# --- create locGuides
def createGuides():
    # # --- modify the main control size
    ControlCurves.scaleCurve(controlNames='C_global0_CNT', scale=1.5)
    ControlCurves.scaleCurve(controlNames='C_god0_CNT', scale=1.5)

    cog = LocGuides.locGuides(name='cog',
                              side='C',
                              size=1,
                              nameList=['cog%s' % i for i in range(1)],
                              color=None,
                              )

def createRig():
    cog = PropCmds.propCmds(side='C',
                            name='cog',
                            guideList=['C_cog%s_GDE' % i for i in range(1)],
                            shape='circle',
                            controlColor=22,
                            controlSize=9,
                            controlRotation=[0, 0, 0],
                            parentJointsTo = 'rubberBallRoot_JNT',
                            jointChain=True)

def cleanup():
    # create
    pass

"""