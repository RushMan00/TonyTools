import pymel.core as pm
import projects.pridapus as pp
import importlib as imp
from rigBuilds import LoadMaFile, BaseRig
imp.reload(LoadMaFile)
imp.reload(BaseRig)


def loadModel():
    # load model
    mainPath = 'D:\OneDrive\TonyTools\Maya\projects\pridapus\model\pridapusMain.ma'
    LoadMaFile.load_ma_file(mainPath)
    # End of load model

    # load setup base
    BaseRig.baseRig(name='pridapus', size=5)
    # End of load model

# def createGuildes():
#
#     # GuidesBuilds.guides()
#     # load Guides data
#     pass
#
# def createRig():
#     # rigs are build on top guides
#     # spineRig.spine()
#     pass
#
# def cleanup():
#     # this is cleanup phase to lock and hide things, and use ishistoricaly intersestiing
#     pass