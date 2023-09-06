import os
import sys
import shutil
import importlib
import traceback
import pymel.core as pm

from rigBuilds import AssetCreator, LoadMaFile, BaseRig, LocGuidesIO, SkinWeightIO, LocGuides, attribute

importlib.reload(AssetCreator)
importlib.reload(LoadMaFile)
importlib.reload(BaseRig)
importlib.reload(LocGuides)
importlib.reload(LocGuidesIO)
importlib.reload(SkinWeightIO)
importlib.reload(attribute)

class riggingUI():
    def __init__(self):
        self.window_name = "Tony Rigging Sys"
        self.window_UI_node = None
        self.paths = r"D:/OneDrive/TonyTools/Maya/projects"
        self.locGuidePaths = r'/data/locGuides'
        self.fullLocGuidePaths = None
        self.skinWeightPaths = r'/data/skinweights'
        self.fullSkinWeightPaths = None
        # self.selected_item = None
        self.folders = None
        self.folderIter = []
        self.module = None
        self.option_menu_for_assets = None
        self.create_asset_window = None
        self.asset_path_text_field = None
        self.selected_item = None
        # init
        self.create_ui_window()

    # --- Step 1 : asset listing and structure creation button
    # Show menu
    def AssetList(self, menu_control):
        "shows a list of current assets"
        # Clear the menu control
        menu_control.deleteAllItems()
        # Get the list of folders in the directory
        self.folders = [folder for folder in os.listdir(self.paths) if
                        os.path.isdir(os.path.join(self.paths, folder))]
        # Add each folder to the menu control
        for folder in self.folders:
            pm.menuItem(label=folder, parent=menu_control)

    def refreshAssetList(self, *args):
        # Refresh the asset list in the UI window
        self.AssetList(self.option_menu_for_assets)
        print("Asset List is refreshed")

    # def createAssetStructure
    def create_asset(self, *args):
        "to create the asset structure to create new assets"
        AssetCreator.AssetCreator(paths=self.paths)
        print("Opening window : Create New Asset Structure")

    # END of Step 1 : asset listing and structure creation button

    # --- Step 2 : Build Meshes Fuction
    # Create a function to handle the button click event
    def build_mesh_callback(self, *args):
        pm.newFile(force=True)
        self.get_selected_asset()
        print(self.selected_item)
        BaseRig.baseRig2(name=self.selected_item,
                         size=5)
        # Load in model
        main_model_paths = self.paths + '\{0}\model\{0}.ma'.format(self.selected_item)
        LoadMaFile.load_ma_file(main_model_paths)
        # Tag all Geos with Skin
        meshes = pm.ls(type='mesh')
        for mesh in meshes:
            attribute.createTags(node=mesh, tagName='skin', tagValue='skinweights')
            if mesh.getParent() != 'GEO':
                pm.parent(mesh, 'GEO')
        print("Build mesh from:", meshes)
    # END OF Step 2 : Build Meshes Fuction

    # --- Step 3 : create LocGuides
    # Create a function to handle the "Build Guides" button click event
    def call_create_guides(self, *args):
        sys.path.append(self.paths + '\\' + self.selected_item)
        self.module = importlib.import_module(self.selected_item)
        importlib.reload(self.module)
        self.module.createGuides()
        print("Loading guides from folder:", self.paths)
        self.fullLocGuidePaths = self.paths + '/' + self.selected_item + '/' + self.locGuidePaths
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
    # END OF Step 3 : Build LocGuides

    # --- Step 4
    # --- Build Rigs
    "build the the rigs from its paths "
    # Create a function to handle the "Build Rigs" button click event
    def build_rigs_callback(self, *args):
        try:
            self.module = importlib.import_module(self.selected_item)
            print("Imported module:", self.module)
            importlib.reload(self.module)
            self.module.createRig()
            print("Called createRig() in module")

            print("Building Rig from folder:", self.paths)

        except Exception as e:
            traceback.print_exc()
            print("Error:", e)

        # apply auto skin
        # self.fullLocGuidePaths = self.paths + '/' + self.selected_item + '/' + self.locGuidePaths
        # loaded = LocGuidesIO.loadLocGuidesData(filePath=self.fullLocGuidePaths)
        # print("Building Rig from folder:", loaded)

    # --- Load Skin
    def load_skins_callback(self, *args):
        self.fullSkinWeightPaths = self.paths + '/' + self.selected_item + '/' + self.skinWeightPaths
        SkinWeightIO.importTaggedSkinWeightMap(self.fullSkinWeightPaths)
        print("load load_skins_callback from folder:")

    # --- Save Skin
    def save_skins_callback(self, *args):
        "save skinweight to path"
        self.fullSkinWeightPaths = self.paths + '/' + self.selected_item + '/' + self.skinWeightPaths
        SkinWeightIO.exportTaggedSkinWeightMap(self.fullSkinWeightPaths)
        print("load save_skins_callback from folder:")

    # --- tag selected Skins
    def tag_skins_callback(self, *args):
        "selected Object will be tagged as skin"
        taggedList = SkinWeightIO.tagAsSkin()
        print(f"Tagging skins :, {taggedList}")

    # --- copy Skinweight to
    def copy_to_skin_callback(self, *args):
        "selected First Object, to copy to second selected object + more"
        SkinWeightIO.copySkinToo()

    # END OF Step 4

    # --- Step 5 : Clean up Rigs
    def clean_up_rig_from_callback(self, *args):
        try:
            self.module = importlib.import_module(self.selected_item)
            print("Imported module:", self.module)
            importlib.reload(self.module)
            self.module.cleanup()
            print("Called cleanup() in module")

            print("Building Rig from folder:", self.paths)

        except Exception as e:
            traceback.print_exc()
            print("Error:", e)
    # --- END OF Step 5 : Clean up Rigs

    def create_ui_window(self):
        """
       creating the Rigging Ui
        :return:
        rigging UI
        """
        # Close existing window
        if self.window_name and pm.window(self.window_name, exists=True):
            pm.deleteUI(self.window_name, window=True)

        # Create UI window
        self.window_UI_node = pm.window(self.window_name, title=self.window_name, widthHeight=(250, 500))
        # Create a form layout
        form_layout = pm.formLayout()

        # --- Step 1 : create Asset Elements
        step1Text = pm.text(label="Step 1: select an asset")
        # Create an optionMenu control
        self.option_menu_for_assets = pm.optionMenu(label="Asset List")
        # Populate the folder list
        self.AssetList(self.option_menu_for_assets)
        # Create a button to refresh the folder list
        refreshButton = pm.button(label="refresh List", command=self.refreshAssetList)
        # Create a button to create the asset
        create_asset_button = pm.button(label="Create Asset", command=self.create_asset)
        # END OF Step 1

        # --- Step 2 : Load meshes
        step2Text = pm.text(label="Step 2 : load in Mesh/Geo")
        # Create a button to build the mesh
        buildMeshButton = pm.button(label="Build Mesh", command=self.build_mesh_callback)
        # END OF Step 2

        # --- Step 3 : Load LocGuides Elements
        step3Text = pm.text(label="Step 3 : load in LocGuides")
        # Create a button to build guides
        build_guides_button = pm.button(label="Build LocGuides", command=self.call_create_guides)
        # build_guides_button = pm.button(label="Build LocGuides", command=self.call_create_guides)
        # Create a button to load guides
        load_guides_button = pm.button(label="Load LocGuides", command=self.load_guides_callback)
        # Create a button to save guides
        save_guides_button = pm.button(label="Save LocGuides", command=self.save_guides_callback)
        # END OF Step 3 : Load LocGuides

        # --- Step 4 : create rigs Elements
        step4Text = pm.text(label="Step 4 : Create Rig")
        build_rigs_button = pm.button(label="Build Rigs", command=self.build_rigs_callback)
        # Create a button to load skins
        load_skin_button = pm.button(label="Load skins", command=self.load_skins_callback)
        # Create a button to save skins
        save_skin_button = pm.button(label="Save skins", command=self.save_skins_callback)
        # Create a button to load skins
        tag_skin_button = pm.button(label="tag skins", command=self.tag_skins_callback)
        # Create a button to save skins
        copy_skin_button = pm.button(label="copy skins to", command=self.copy_to_skin_callback)
        # END OF Step 4 : create rigs

        # --- clean up rigs
        step5Text = pm.text(label="Step 5 : FINAL")
        cleanup_button = pm.button(label="clean up Rig", command=self.clean_up_rig_from_callback)

        # Position the UI elements within the form layout
        pm.formLayout(form_layout, edit=True,
                      attachForm=[
                          # --- Step 1 : Asset list and Element position
                          (step1Text, 'top', 20),
                          (step1Text, "left", 10),
                          (step1Text, "right", 10),

                          (self.option_menu_for_assets, "left", 10),
                          (self.option_menu_for_assets, "right", 10),

                          (refreshButton, "left", 10),
                          (create_asset_button, "right", 10),

                          # --- Step 2 : Meshes Element position
                          (step2Text, "left", 10),
                          (step2Text, "right", 10),

                          (buildMeshButton, "left", 10),
                          (buildMeshButton, "right", 10),

                          # --- Step 3 : LocGuides Element position
                          (step3Text, "left", 10),
                          (step3Text, "right", 10),

                          (build_guides_button, "left", 10),
                          (build_guides_button, "right", 10),

                          (load_guides_button, "left", 10),
                          (save_guides_button, "right", 10),

                          # --- Step 4 : Build Rigs Element position
                          (step4Text, "left", 10),
                          (step4Text, "right", 10),

                          (build_rigs_button, "left", 10),
                          (build_rigs_button, "right", 10),

                          (load_skin_button, "left", 10),
                          (save_skin_button, "right", 10),

                          (tag_skin_button, "left", 10),
                          (copy_skin_button, "right", 10),

                          # --- Step 5 : FINALIZE Rigs Element position
                          (step5Text, "left", 10),
                          (step5Text, "right", 10),
                          (cleanup_button, "left", 10),
                          (cleanup_button, "right", 10),
                      ],
                      attachControl=[
                          # --- Step 1 : Asset list Elements
                          (self.option_menu_for_assets, "top", 10, step1Text),
                          (refreshButton, "top", 10, self.option_menu_for_assets),
                          (refreshButton, "right", 20, create_asset_button),
                          (create_asset_button, "top", 10, self.option_menu_for_assets),

                          # --- Step 2 : Meshes Element
                          (step2Text, "top", 20, create_asset_button),
                          (buildMeshButton, "top", 10, step2Text),

                          # --- Step 3 :  LocGuides Element
                          (step3Text, "top", 20, buildMeshButton),
                          (build_guides_button, "top", 10, step3Text),
                          (load_guides_button, "top", 10, build_guides_button),
                          (save_guides_button, "top", 10, build_guides_button),
                          (save_guides_button, "left", 10, load_guides_button),

                          # --- Step 4 :  Build Rig Element
                          (step4Text, "top", 20, load_guides_button),
                          (build_rigs_button, "top", 10, step4Text),
                          (load_skin_button, "top", 10, build_rigs_button),
                          (save_skin_button, "top", 10, build_rigs_button),

                          (save_skin_button, "left", 10, load_skin_button),

                          (tag_skin_button, "top", 10, load_skin_button),
                          (copy_skin_button, "top", 10, save_skin_button),

                          # --- Step 5 :  Finalizing
                          (step5Text, "top", 20, tag_skin_button),
                          (cleanup_button, "top", 10, step5Text),

                      ])

        # Show the UI window
        pm.showWindow(self.window_UI_node)

    # def __repr__(self):
    #     return pm.lsUI(type="window")
