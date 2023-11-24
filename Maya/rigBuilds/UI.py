import os
import sys
import shutil
import importlib
import traceback

import maya.cmds as cmds
import pymel.core as pm

from rigBuilds import AssetCreator, LoadMaFile, BaseRig, LocGuides, LocGuidesIO, SkinWeightIO, attribute

importlib.reload(AssetCreator)
importlib.reload(LoadMaFile)
importlib.reload(BaseRig)
importlib.reload(LocGuides)
importlib.reload(LocGuidesIO)
importlib.reload(SkinWeightIO)
importlib.reload(attribute)

from rigBuilds.rig import Joints
importlib.reload(Joints)

class riggingUI():
    def __init__(self):
        self.windowName = "Tony Rigging Sys"
        self.windowUINode = None
        self.paths = r"D:/OneDrive/TonyTools/Maya/projects"
        self.locGuidePaths = r'/data/locGuides'
        self.fullLocGuidePaths = None
        self.skinWeightPaths = r'/data/skinweights'
        self.fullSkinWeightPaths = None
        # self.selectedItem = None
        self.folders = None
        self.folderIter = []
        self.module = None
        self.optionMenuForAssets = None
        # self.create_asset_window = None
        # self.asset_path_text_field = None
        self.selectedItem = None
        # init
        self.create_ui_window()

    # --- Step 1 : asset listing and structure creation button
    # Show menu
    def AssetList(self, menu_control):
        "shows a list of current assets"
        # Clear the menu control
        if cmds.menu(menu_control, exists=True):
            items = cmds.menu(menu_control, query=True, itemArray=True) or []
            for item in items:
                cmds.deleteUI(item)

        # Get the list of folders in the directory
        self.folders = [folder for folder in os.listdir(self.paths) if
                        os.path.isdir(os.path.join(self.paths, folder))]
        # Add each folder to the menu control
        for folder in self.folders:
            cmds.menuItem(label=folder, parent=menu_control)

    def getCurrentAssetFromList(self, *args):
        "to select the current item on the asset list"
        self.selectedItem = cmds.optionMenu(self.optionMenuForAssets, query=True, value=True)
        print("Selected Item:", self.selectedItem)

    def refreshAssetList(self, *args):
        # Refresh the asset list in the UI window
        self.AssetList(self.optionMenuForAssets)
        print("Asset List is refreshed")

    # def createAssetStructure
    def create_asset(self, *args):
        "to create the asset structure to create new assets"
        AssetCreator.AssetCreator(paths=self.paths)
        print("Opening window : Create New Asset Structure")
    # END of Step 1 : asset listing and structure creation button

    # --- Build Meshes Fuction
    # Create a function to handle the button click event
    def build_mesh_callback(self, *args):
        cmds.file(force=True, new=True)
        self.getCurrentAssetFromList()
        print(self.selectedItem)
        BaseRig.baseRig2(name=self.selectedItem,
                         size=5)
        LoadMaFile.loadMaFile(self.paths + '/{0}/model/{0}.ma'.format(self.selectedItem))
        # Tag all Geos with Skin
        meshes = cmds.ls(type='mesh')
        meshesTransforms = [cmds.listRelatives(mesh, parent=True)[0] for mesh in meshes]
        for mesh in meshesTransforms:
            attribute.createTags(nodeName=mesh, attrName='skin', attrValue='skinweights')
            cmds.parent(mesh, 'GEO')
            print("Build mesh from:", mesh)
    # END OF Build Meshes Fuction

    # --- Step 2 : create LocGuides
    # Create a function to handle the "Build Guides" button click event
    def call_create_guides(self, *args):
        self.build_mesh_callback()
        sys.path.append(self.paths + '\\' + self.selectedItem)
        self.module = importlib.import_module(self.selectedItem)
        importlib.reload(self.module)
        self.module.createGuides()
        print("Loading guides from folder:", self.paths)
        self.fullLocGuidePaths = self.paths + '/' + self.selectedItem + '/' + self.locGuidePaths
        loaded = LocGuidesIO.loadLocGuidesData(filePath=self.fullLocGuidePaths)
        print("Loading data from folder:", loaded)

    # function to handle the "Load Guides" button click event
    def load_guides_callback(self, *args):
        loaded = LocGuidesIO.loadLocGuidesData(filePath=self.fullLocGuidePaths)
        print("Loading guides from folder:", loaded)

    # function to handle the "Save Guides" button click event
    def save_guides_callback(self, *args):
        dataList = LocGuidesIO.writeLocGuidesData(tagName='locator', filePath=self.fullLocGuidePaths)
        print("Saving guides to folder:", dataList)
    # END OF Step 2 : Build LocGuides

    # --- Step 3
    # --- Build Rigs
    "build the the rigs from its paths "
    # Create a function to handle the "Build Rigs" button click event
    def build_rigs_callback(self, *args):
        try:
            self.module = importlib.import_module(self.selectedItem)
            print("Imported module:", self.module)
            importlib.reload(self.module)
            self.module.createRig()
            print("Called createRig() in module")

            print("Building Rig from folder:", self.paths)

        except Exception as e:
            traceback.print_exc()
            print("Error:", e)

        # apply auto skin after building rig
        self.fullSkinWeightPaths = self.paths + '/' + self.selectedItem + '/' + self.skinWeightPaths
        loaded = SkinWeightIO.importTaggedSkinWeightMap(filePath=self.fullSkinWeightPaths)
        print("Building Rig from folder:", loaded)

    # --- Load Skin
    def load_skins_callback(self, *args):
        self.fullSkinWeightPaths = self.paths + '/' + self.selectedItem + '/' + self.skinWeightPaths
        SkinWeightIO.importTaggedSkinWeightMap(self.fullSkinWeightPaths)
        print("load load_skins_callback from folder:")

    # --- Save Skin
    def save_skins_callback(self, *args):
        "save skinweight to path"
        self.fullSkinWeightPaths = self.paths + '/' + self.selectedItem + '/' + self.skinWeightPaths
        SkinWeightIO.exportTaggedSkinWeightMap(self.fullSkinWeightPaths)
        print("load save_skins_callback from folder:")

    # --- tag selected Skins
    def tag_skins_callback(self, *args):
        "selected Object will be tagged as skin"
        taggedList = SkinWeightIO.tagAsSkin()
        print(f"Tagging skins :, {taggedList}")

    # --- select tagged joints
    def selectTaggedJointsCallback(self, *args):
        "selected Object is tagged as joints"
        taggedList = Joints.selectTaggedJoints()

    # --- copy Skinweight to
    def copy_to_skin_callback(self, *args):
        "selected First Object, to copy to second selected object + more"
        SkinWeightIO.copySkinToo()

    # END OF Step 3

    # --- Step 4 : Clean up Rigs
    def clean_up_rig_from_callback(self, *args):
        try:
            self.module = importlib.import_module(self.selectedItem)
            print("Imported module:", self.module)
            importlib.reload(self.module)
            self.module.cleanup()
            print("Called cleanup() in module")

            print("activating Cleaning up Rig from folder:", self.paths)

        except Exception as e:
            traceback.print_exc()
            print("Error:", e)
    # --- END OF Step 4 : Clean up Rigs

    def create_ui_window(self):
        """
       creating the Rigging Ui
        :return:
        rigging UI
        """
        # Close existing window
        if self.windowName and cmds.window(self.windowName, exists=True):
            cmds.deleteUI(self.windowName, window=True)

        # Create UI window
        self.windowUINode = cmds.window(self.windowName, title=self.windowName, widthHeight=(250, 500))
        # Create a form layout
        form_layout = cmds.formLayout()

        # --- Step 1 : create Asset Elements
        step1Text = cmds.text(label="Step 1: select an asset")
        # Create an optionMenu control
        self.optionMenuForAssets = cmds.optionMenu(label="Asset List")
        # Populate the folder list
        self.AssetList(self.optionMenuForAssets)
        # Create a button to refresh the folder list
        refreshButton = cmds.button(label="refresh List", command=self.refreshAssetList)
        # Create a button to create the asset
        create_asset_button = cmds.button(label="Create Asset", command=self.create_asset)
        # END OF Step 1

        # # --- Step 2 : Load meshes
        # step2Text = cmds.text(label="Step 2 : load in Mesh/Geo")
        # # Create a button to build the mesh
        # buildMeshButton = cmds.button(label="Build Mesh", command=self.build_mesh_callback)
        # # END OF Step 2

        # --- Step 3 : Load LocGuides Elements
        step2Text = cmds.text(label="Step 2 : load in LocGuides")
        # Create a button to build guides
        build_guides_button = cmds.button(label="Build LocGuides", command=self.call_create_guides)
        # Create a button to load guides
        load_guides_button = cmds.button(label="Load LocGuides", command=self.load_guides_callback)
        # Create a button to save guides
        save_guides_button = cmds.button(label="Save LocGuides", command=self.save_guides_callback)
        # END OF Step 3 : Load LocGuides

        # --- Step 4 : create rigs Elements
        step3Text = cmds.text(label="Step 3 : Create Rig")
        build_rigs_button = cmds.button(label="Build Rigs", command=self.build_rigs_callback)
        # Create a button to load skins
        load_skin_button = cmds.button(label="Load skins", command=self.load_skins_callback)
        # # Create a button to save skins
        save_skin_button = cmds.button(label="Save skins", command=self.save_skins_callback)

        skinningToolsText = cmds.text(label="skinning tools")
        # Create a button to load skins
        tag_skin_button = cmds.button(label="tag as skins", command=self.tag_skins_callback)
        # Create a button to load skins
        selectTaggedJointsButton = cmds.button(label="Select Tagged Joints", command=self.selectTaggedJointsCallback)
        # Create a button to save skins
        copy_skin_button = cmds.button(label="copy skins to (select toggle)", command=self.copy_to_skin_callback)
        # END OF Step 4 : create rigs

        # --- clean up rigs
        step4Text = cmds.text(label="Step 4 : FINAL")
        cleanup_button = cmds.button(label="clean up Rig", command=self.clean_up_rig_from_callback)

        # Position the UI elements within the form layout
        cmds.formLayout(form_layout, edit=True,
                      attachForm=[
                          # --- Step 1 : Asset list and Element position
                          (step1Text, 'top', 20),
                          (step1Text, "left", 10),
                          (step1Text, "right", 10),

                          (self.optionMenuForAssets, "left", 10),
                          (self.optionMenuForAssets, "right", 10),

                          (refreshButton, "left", 10),
                          (create_asset_button, "right", 10),

                          # --- Step 2 : LocGuides Element position
                          (step2Text, "left", 10),
                          (step2Text, "right", 10),

                          (build_guides_button, "left", 10),
                          (build_guides_button, "right", 10),

                          (load_guides_button, "left", 10),
                          (save_guides_button, "right", 10),

                          # --- Step 3 : Create Rigs Element position
                          (step3Text, "left", 10),
                          (step3Text, "right", 10),

                          (build_rigs_button, "left", 10),
                          (build_rigs_button, "right", 10),

                          (load_skin_button, "left", 10),
                          (save_skin_button, "right", 10),

                          (skinningToolsText, "left", 10),
                          (skinningToolsText, "right", 10),

                          (tag_skin_button, "left", 10),
                          (selectTaggedJointsButton, "left", 10),

                          (copy_skin_button, "right", 10),

                          # --- Step 4 : FINALIZE Rigs Element position
                          (step4Text, "left", 10),
                          (step4Text, "right", 10),
                          (cleanup_button, "left", 10),
                          (cleanup_button, "right", 10),
                      ],
                      attachControl=[
                          # --- Step 1 : Asset list Elements
                          (self.optionMenuForAssets, "top", 10, step1Text),
                          (refreshButton, "top", 10, self.optionMenuForAssets),
                          (refreshButton, "right", 20, create_asset_button),
                          (create_asset_button, "top", 10, self.optionMenuForAssets),

                          # # --- Step 2 : Meshes Element
                          # (step2Text, "top", 20, create_asset_button),
                          # (buildMeshButton, "top", 10, step2Text),

                          # --- Step 2 :  LocGuides Element
                          (step2Text, "top", 20, create_asset_button),
                          (build_guides_button, "top", 10, step2Text),
                          (load_guides_button, "top", 10, build_guides_button),
                          (save_guides_button, "top", 10, build_guides_button),
                          (save_guides_button, "left", 10, load_guides_button),

                          # --- Step 3 :  create Rig Element
                          (step3Text, "top", 20, load_guides_button),
                          (build_rigs_button, "top", 10, step3Text),
                          (load_skin_button, "top", 10, build_rigs_button),

                          (save_skin_button, "top", 10, build_rigs_button),
                          (save_skin_button, "left", 10, load_skin_button),

                          (skinningToolsText, "top", 10, load_skin_button),

                          (tag_skin_button, "top", 10, skinningToolsText),
                          (selectTaggedJointsButton, "top", 10, tag_skin_button),
                          (copy_skin_button, "top", 10, skinningToolsText),

                          # --- Step 4 :  Finalizing
                          (step4Text, "top", 20, selectTaggedJointsButton),
                          (cleanup_button, "top", 10, step4Text),

                      ])

        # Show the UI window
        cmds.showWindow(self.windowUINode)

    # def __repr__(self):
    #     return cmds.lsUI(type="window")
