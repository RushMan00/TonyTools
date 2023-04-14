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
    BaseRig.baseRig(name='pridapus',
                    size=1,
                    children=['GEO', 'RIG', 'SKELE'],
                    nestingGrp={'RIG': ['C_main_GRP','C_global_GRP', 'C_globalBuffer_GRP','C_global_CTL', 'C_globalGimbal_CTL'],
                                'GEO': ['C_main1_GRP', 'C_mainBuffer0_GRP'],
                                'SKELE': ['C_main2_GRP','C_mainBuffer2_GRP']},
                    )
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