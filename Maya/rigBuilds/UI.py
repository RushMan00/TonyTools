import os
import pymel.core as pm
import importlib as imp

from rigBuilds import LoadMaFile, BaseRig, LocGuidesIO, LocGuides, attribute
imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)
imp.reload(attribute)

import projects.pridapus.pridapusMain as work
imp.reload(work)


# the directory path
windowName='Tony Rigging System'
directory_path = r"D:\OneDrive\TonyTools\Maya\projects"
idx = []
fld = []
selected_folder = ""  # Declare the global variable
optionMenuForAssets = None  # Declare the global variable


# Create a function to populate the list
def AssetList(menu_control):
    # Clear the menu control
    menu_control.deleteAllItems()
    # Get the list of folders in the directory
    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]
    # Add each folder to the menu control
    for folder in folders:
        pm.menuItem(label=folder, parent=menu_control)

# Create a function to handle the button click event
def buildMeshCallback(*args):
    global selected_folder  # Use the global variable
    AssetList(optionMenuForAssets)
    # load setup base
    print(fld)
    print(idx)
    # BaseRig.baseRig(name=fld[0],
    #                 groups={
    #                     'GEO': [],
    #                     'RIG': ['C_main_GRP', 'C_global_CTL', 'C_globalGimbal_CTL', 'C_local_GRP'],
    #                     'SKELE': []
    #                 },
    #                 size=5)

    # # load in model
    # mainPath = directory_path + '\pridapus' + '\model\pridapusMain.ma'
    # LoadMaFile.load_ma_file(mainPath)

    # # tag All Geos With Skin
    # meshes = pm.ls(type='mesh')
    # for mesh in meshes:
    #     attribute.createTags(node=mesh, tagName='skin', tagValue='skinweights')
        # pm.parent(mesh, 'GEO')
    # selected_folder = pm.optionMenu(jnt, query=True, value=True)
    # print("Build mesh form :" + meshes)

# Create a function to handle the "Build Guides" button click event
def build_guides_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("Building guides in folder:", selected_folder)

# Create a function to handle the "Load Guides" button click event
def load_guides_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("Loading guides from folder:", selected_folder)

# Create a function to handle the "Save Guides" button click event
def save_guides_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("Saving guides to folder:", selected_folder)

# Create a function to handle the "Build Rigs" button click event
def build_rigs_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("Building rigs in folder:", selected_folder)

# --- Skin Section
def load_skins_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("load skins from folder:", selected_folder)

def save_skins_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("load skins from folder:", selected_folder)

def tag_skins_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("tagging skins in scene:", selected_folder)

def copy_skins_from_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("copying skins from place name here :", selected_folder)

def clean_up_rig_from_callback(*args):
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("cleaning up rig :", selected_folder)

def close_existing_window():
    if pm.window(windowName, exists=True):
        pm.deleteUI(windowName, window=True)

# Function to create the UI window
def create_ui_window():
    global selected_folder, optionMenuForAssets
    close_existing_window()
    # --- make UI window
    if not pm.window(windowName, exists=True):
        window = pm.window(title=windowName, widthHeight=(250, 500))
        # Create a form layout
        form_layout = pm.formLayout()

        # --- Assets
        step1Text = pm.text(label="Step 1 : select an asset")
        # Create an optionMenu control
        optionMenuForAssets = pm.optionMenu(label="Asset List")
        # Populate the folder list
        AssetList(optionMenuForAssets)

        selected_index = pm.optionMenu(optionMenuForAssets, query=True, select=True)
        idx.append(selected_index)
        selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
        fld.append(selected_folder)

        # Create a button to refresh the folder list
        refreshButton = pm.button(label="Refresh", command=lambda args: AssetList(optionMenuForAssets))
        # Create a button to create the asset
        create_asset_button = pm.button(label="Create Asset", command=build_rigs_callback)

        # --- Load meshes
        step2Text = pm.text(label="Step 2 : load in Mesh/Geo")
        # Create a button to build the mesh
        buildMeshButton = pm.button(label="Build Mesh", command=buildMeshCallback)

        # --- create guides
        step3Text = pm.text(label="Step 3 : load in LocGuides")
        # Create a button to build guides
        build_guides_button = pm.button(label="Build LocGuides", command=build_guides_callback)
        # Create a button to load guides
        load_guides_button = pm.button(label="Load LocGuides", command=load_guides_callback)
        # Create a button to save guides
        save_guides_button = pm.button(label="Save LocGuides", command=save_guides_callback)

        # --- create rigs
        step4Text = pm.text(label="Step 4 : Create the Rig")
        build_rigs_button = pm.button(label="Build Rigs", command=build_rigs_callback)
        # Create a button to load skins
        load_skin_button = pm.button(label="Load skins", command=load_skins_callback)
        # Create a button to save skins
        save_skin_button = pm.button(label="Save skins", command=save_skins_callback)
        # Create a button to load skins
        tag_skin_button = pm.button(label="tag skins", command=load_skins_callback)
        # Create a button to save skins
        copy_skin_button = pm.button(label="copy skins to", command=save_skins_callback)

        # --- create rigs
        step5Text = pm.text(label="Step 5 : FINAL")
        cleanup_button = pm.button(label="clean up Rig", command=clean_up_rig_from_callback)

        # Position the UI elements within the form layout
        pm.formLayout(form_layout, edit=True,
                      attachForm=[
                                  # Asset List
                                  (step1Text, 'top', 20),
                                  (step1Text, "left", 10),
                                  (step1Text, "right", 10),

                                  (optionMenuForAssets, "left", 10),
                                  (optionMenuForAssets, "right", 10),

                                  # refresh button
                                  (refreshButton, "left", 10),
                                  (create_asset_button, "right", 10),

                                  # Build Meshes
                                  (step2Text, "left", 10),
                                  (step2Text, "right", 10),

                                  (buildMeshButton, "left", 10),
                                  (buildMeshButton, "right", 10),

                                  # Build Locator Guides
                                  (step3Text, "left", 10),
                                  (step3Text, "right", 10),

                                  (build_guides_button, "left", 10),
                                  (build_guides_button, "right", 10),

                                  (load_guides_button, "left", 10),
                                  (save_guides_button, "right", 10),

                                   # Build Rig
                                  (step4Text, "left", 10),
                                  (step4Text, "right", 10),

                                  (build_rigs_button, "left", 10),
                                  (build_rigs_button, "right", 10),

                                  (load_skin_button, "left", 10),
                                  (save_skin_button, "right", 10),
                                  (tag_skin_button, "left", 10),
                                  (copy_skin_button, "right", 10),

                                  # FINAL
                                  (step5Text, "left", 10),
                                  (step5Text, "right", 10),
                                  (cleanup_button, "left", 10),
                                  (cleanup_button, "right", 10),
                                  ],

                      attachControl=[
                                    # Asset List
                                    (optionMenuForAssets, "top", 10, step1Text),
                                    (refreshButton, "top", 10, optionMenuForAssets),
                                    (refreshButton, "right", 20, create_asset_button),
                                    (create_asset_button, "top", 10, optionMenuForAssets),

                                    # Build Meshes
                                    (step2Text, "top", 20, create_asset_button),
                                    (buildMeshButton, "top", 10, step2Text),

                                    #
                                    (step3Text, "top", 20, buildMeshButton),
                                    (build_guides_button, "top", 10, step3Text),
                                    (load_guides_button, "top", 10, build_guides_button),
                                    (save_guides_button, "top", 10, build_guides_button),


                                    (step4Text, "top", 20, load_guides_button),
                                    (build_rigs_button, "top", 10, step4Text),
                                    (load_skin_button, "top", 10, build_rigs_button),
                                    (save_skin_button, "top", 10, build_rigs_button),
                                    (tag_skin_button, "top", 10, load_skin_button),
                                    (copy_skin_button, "top", 10, save_skin_button),

                                     # FINAL
                                    (step5Text, "top", 20, tag_skin_button),
                                    (cleanup_button, "top", 10, step5Text),
                                    ]
                                    )
        # Show the UI window
        window.show()

create_ui_window()