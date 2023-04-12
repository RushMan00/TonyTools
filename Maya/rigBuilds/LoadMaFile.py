import pymel.core as pm

def load_ma_file(filepath):
    """
    Loads a Maya ASCII (.ma) file into the current Maya session.
    Returns True if the file was loaded successfully, False otherwise.
    """
    try:
        pm.importFile(filepath, type="mayaAscii", ignoreVersion=True)
        return True
    except:
        pm.warning("Failed to load file: {}".format(filepath))
        return False