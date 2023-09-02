import os
import shutil
import pymel.core as pm

def create_asset_folder(self, *args):
    asset_path = pm.textField(self.asset_path_text_field, query=True, text=True)

    # Check if the path ends with .ma or .mb
    if not asset_path.endswith(".ma") and not asset_path.endswith(".mb"):
        pm.warning("Please make sure the Asset Path ends with .ma or .mb")
        return

    # Check if the file exists
    if not os.path.exists(asset_path):
        pm.warning("The file does not exist at the provided path.")
        return

    asset_name = os.path.splitext(os.path.basename(asset_path))[0]
    asset_folder_path = os.path.join(self.paths, asset_name)

    # Check if the asset folder already exists
    if os.path.exists(asset_folder_path):
        pm.warning(f"The asset folder '{asset_name}' already exists. Please choose a different asset name.")
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
        python_file.write("# Python file for asset")

    # Create the locGuides and skinweights folders under data folder
    loc_guides_folder_path = os.path.join(data_folder_path, "locGuides")
    skin_weights_folder_path = os.path.join(data_folder_path, "skinweights")
    os.makedirs(loc_guides_folder_path)
    os.makedirs(skin_weights_folder_path)

    # Copy asset file to the model folder
    model_asset_path = os.path.join(model_folder_path, os.path.basename(asset_path))
    shutil.copy(asset_path, model_asset_path)
    print("Copied asset file to the model folder.")

    # Refresh the asset list in the UI window
    self.AssetList(self.option_menu_for_assets)


def create_asset_window(self):
    if self.create_asset_window and pm.window(self.create_asset_window, exists=True):
        pm.deleteUI(self.create_asset_window, window=True)

    self.create_asset_window = pm.window("Create New Asset", title="Create New Asset", widthHeight=(300, 120))
    create_asset_layout = pm.columnLayout(adjustableColumn=True)

    pm.text(label="Asset Path (with .ma or .mb extension):")
    self.asset_path_text_field = pm.textField()
    pm.button(label="Create Asset Structure", command=self.create_asset_folder)

    pm.setParent('..')
    pm.showWindow(self.create_asset_window)