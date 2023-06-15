import os
import pymel.core as pm

# Define the directory path
windowName='Tony Rigging System'
directory_path = r"D:\OneDrive\TonyTools\Maya\projects"

# Create a function to populate the list
def populate_folder_list(menu_control):
    # Clear the menu control
    menu_control.deleteAllItems()

    # Get the list of folders in the directory
    folders = [folder for folder in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, folder))]

    # Add each folder to the menu control
    for folder in folders:
        pm.menuItem(label=folder, parent=menu_control)

# Create a function to handle the button click event
def build_mesh_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("Build mesh for folder:", selected_folder)

# Create a function to handle the "Build Guides" button click event
def build_guides_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("Building guides in folder:", selected_folder)

# Create a function to handle the "Load Guides" button click event
def load_guides_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("Loading guides from folder:", selected_folder)

# Create a function to handle the "Save Guides" button click event
def save_guides_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("Saving guides to folder:", selected_folder)

# Create a function to handle the "Build Rigs" button click event
def build_rigs_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("Building rigs in folder:", selected_folder)

# --- Skin Section
def load_skins_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("load skins from folder:", selected_folder)

def save_skins_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("load skins from folder:", selected_folder)

def tag_skins_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("tagging skins in scene:", selected_folder)

def copy_skins_from_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("copying skins from place name here :", selected_folder)

def clean_up_rig_from_callback(*args):
    selected_folder = pm.optionMenu(option_menu, query=True, value=True)
    print("cleaning up rig :", selected_folder)


# Function to close the existing UI window
def close_existing_window():
    if pm.window(windowName, exists=True):
        pm.deleteUI(windowName, window=True)

# Function to create the UI window
def create_ui_window():
    # Close the existing window if it exists
    close_existing_window()
    # Create the UI window
    window = pm.window(title=windowName, widthHeight=(250, 350))

    # Create a form layout
    form_layout = pm.formLayout()

    # Create a button to create the asset
    create_asset_button = pm.button(label="Create Asset", command=build_rigs_callback)

    # Create an optionMenu control
    option_menu = pm.optionMenu(label="Asset")

    # Populate the folder list
    populate_folder_list(option_menu)

    # Create a button to refresh the folder list
    refresh_button = pm.button(label="Refresh", command=lambda args: populate_folder_list(option_menu))

    # Create a button to build the mesh
    build_mesh_button = pm.button(label="Build Mesh", command=build_mesh_callback)

    # Create a button to build guides
    build_guides_button = pm.button(label="Build Guides", command=build_guides_callback)

    # Create a button to load guides
    load_guides_button = pm.button(label="Load Guides", command=load_guides_callback)

    # Create a button to save guides
    save_guides_button = pm.button(label="Save Guides", command=save_guides_callback)

    # Create a button to build rigs
    build_rigs_button = pm.button(label="Build Rigs", command=build_rigs_callback)

    # Create a button to load skins
    load_skin_button = pm.button(label="Load skins", command=load_skins_callback)
    # Create a button to save skins
    save_skin_button = pm.button(label="Save skins", command=save_skins_callback)
    # Create a button to load skins
    tag_skin_button = pm.button(label="tag skins", command=load_skins_callback)
    # Create a button to save skins
    copy_skin_button = pm.button(label="copy skins to", command=save_skins_callback)

    cleanup_button = pm.button(label="clean up Rig", command=clean_up_rig_from_callback)

    # Position the UI elements within the form layout
    pm.formLayout(form_layout, edit=True,
                  attachForm=[
                              (create_asset_button, "top", 10),
                              (create_asset_button, "left", 10),
                              (create_asset_button, "right", 10),

                              (option_menu, "left", 10),
                              (option_menu, "right", 10),

                              (refresh_button, "left", 10),
                              (refresh_button, "right", 10),

                              (build_mesh_button, "left", 10),
                              (build_mesh_button, "right", 10),

                              (build_guides_button, "left", 10),
                              (build_guides_button, "right", 10),

                              (load_guides_button, "left", 10),
                              (save_guides_button, "right", 10),

                              (build_rigs_button, "left", 10),
                              (build_rigs_button, "right", 10),

                              (load_skin_button, "left", 10),
                              (save_skin_button, "right", 10),
                              (tag_skin_button, "left", 10),
                              (copy_skin_button, "right", 10),

                              (cleanup_button, "left", 10),
                              (cleanup_button, "right", 10),
                              ],
                  attachControl=[
                                (option_menu, "top", 10, create_asset_button),
                                (refresh_button, "top", 10, option_menu),
                                (build_mesh_button, "top", 10, refresh_button),
                                (build_guides_button, "top", 10, build_mesh_button),
                                (load_guides_button, "top", 10, build_guides_button),
                                (save_guides_button, "top", 10, build_guides_button),
                                (build_rigs_button, "top", 10, save_guides_button),
                                (load_skin_button, "top", 10, build_rigs_button),
                                (save_skin_button, "top", 10, build_rigs_button),
                                (tag_skin_button, "top", 10, load_skin_button),
                                (copy_skin_button, "top", 10, save_skin_button),
                                (cleanup_button, "top", 10, copy_skin_button),
                                ]
                                )

    # Show the UI window
    window.show()

# Create the UI window
create_ui_window()