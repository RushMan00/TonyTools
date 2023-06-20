import os
import pymel.core as pm
import importlib as imp
import sys

# sys.path.append('D:\OneDrive\TonyTools\Maya')
# paths = sys.path
# for i in paths:
#     print(i)
#
# import rigBuilds.startupRigBuilds as surb
# surb.importingPaths()
# # import project
# import projects.pridapus.pridapusMain as work
# imp.reload(work)

# Define the directory path
windowName='Tony Rigging System'
directory_path = r"D:\OneDrive\TonyTools\Maya\projects"

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
    selected_folder = pm.optionMenu(optionMenuForAssets, query=True, value=True)
    print("Build mesh for folder:", selected_folder)

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


# Function to close the existing UI window
def close_existing_window():
    if pm.window(windowName, exists=True):
        pm.deleteUI(windowName, window=True)

# Function to create the UI window
def create_ui_window():
    # --- make UI window
    # Close the existing window if it exists
    close_existing_window()
    # Create the UI window
    window = pm.window(title=windowName, widthHeight=(250, 500))
    # Create a form layout
    form_layout = pm.formLayout()

    # --- Assets
    step1Text = pm.text(label="Step 1 : select an asset")
    # Create an optionMenu control
    optionMenuForAssets = pm.optionMenu(label="Asset List")
    # Populate the folder list
    AssetList(optionMenuForAssets)
    # Create a button to refresh the folder list
    refresh_button = pm.button(label="Refresh", command=lambda args: AssetList(optionMenuForAssets))
    # Create a button to create the asset
    create_asset_button = pm.button(label="Create Asset", command=build_rigs_callback)

    # --- Load meshes
    step2Text = pm.text(label="Step 2 : load in Mesh/Geo")
    # Create a button to build the mesh
    build_mesh_button = pm.button(label="Build Mesh", command=buildMeshCallback)

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
                              # (optionMenuForAssets, 'top', 20),
                              (optionMenuForAssets, "left", 10),
                              (optionMenuForAssets, "right", 10),
                              # refresh button
                              (refresh_button, "left", 10),
                              (create_asset_button, "right", 10),

                              # Build Meshes
                              (step2Text, "left", 10),
                              (step2Text, "right", 10),

                              (build_mesh_button, "left", 10),
                              (build_mesh_button, "right", 10),

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
                                (refresh_button, "top", 10, optionMenuForAssets),
                                (refresh_button, "right", 20, create_asset_button),
                                (create_asset_button, "top", 10, optionMenuForAssets),
                                # Build Meshes
                                (step2Text, "top", 20, create_asset_button),
                                (build_mesh_button, "top", 10, step2Text),

                                (step3Text, "top", 20, build_mesh_button),
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

# Create the UI window
create_ui_window()