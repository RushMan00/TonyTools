import pymel.core as pm
import importlib as imp
from rigBuilds import LoadMaFile, BaseRig, LocGuidesIO, LocGuides
imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)

# --- Backend
paths = 'D:\OneDrive\TonyTools\Maya\projects\pridapus'

def loadModel():
    # load setup base
    BaseRig.baseRig(name='pridapus', size=5)
    # load model
    mainPath = paths + '\model\pridapusMain.ma'
    LoadMaFile.load_ma_file(mainPath)
    # End of load model

def createGuildes():
    # --- create locGuides
    spine = LocGuides.locGuides(
                                name='spine',
                                side='C',
                                size=1,
                                numberOfGuides=5,
                                color=None,
                                asChain = False,
                                )

    arm = LocGuides.locGuides(
                                name='arm',
                                side='L',
                                size=1,
                                numberOfGuides=3,
                                color=None,
                                asChain=False,
                                mirror=True,
                                mirrorRotatoin=True,
                            )
    leg = LocGuides.locGuides(
                                name='leg',
                                side='L',
                                size=1,
                                numberOfGuides=3,
                                color=None,
                                asChain=False,
                                mirror=True,
                                mirrorRotatoin=True,
                            )

    # # load last saved guide data
    # loaded = LocGuidesIO.loadLocGuidesData(filePath=paths + '\data\locGuides')
def loadGuildes():
     loaded = LocGuidesIO.loadLocGuidesData(filePath=paths + '\data\locGuides')
def saveGuildes():
    dataList = LocGuidesIO.writeLocGuidesData(tagName='locator', filePath=paths + '\data\locGuides')

def createRig():
    # rigs are build on top locGuides
    # spineRig.spine()
    pass

# def cleanup():
#     # this is cleanup phase to lock and hide things, and use ishistoricaly intersestiing
#     pass