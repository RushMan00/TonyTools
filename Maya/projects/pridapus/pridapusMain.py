import pymel.core as pm
import importlib as imp
from rigBuilds import LoadMaFile, BaseRig, LocGuidesIO, LocGuides, attribute

imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)
imp.reload(attribute)

# --- Backend
paths = 'D:\OneDrive\TonyTools\Maya\projects\pridapus'

def loadModel():
    # load setup base
    BaseRig.baseRig(name='pridapus',
                    groups={
                            'GEO': [],
                            'RIG': ['C_main_GRP', 'C_global_CTL', 'C_globalGimbal_CTL', 'C_local_GRP'],
                            'SKELE': []
                    },
                    size=5)
    # load model
    mainPath = paths + '\model\pridapusMain.ma'
    LoadMaFile.load_ma_file(mainPath)
    meshes = pm.ls(type='mesh')
    # tag All Geos With Skin
    for mesh in meshes:
        attribute.createTags(node=mesh, tagName='skin', tagValue='skinweights')
        pm.parent(mesh, 'GEO')
    # end of loadModel

def createGuildes():
    # --- create locGuides
    spine = LocGuides.locGuides(
                                name='spine',
                                side='C',
                                size=1,
                                guideList=['spine%s' % i for i in range(5)],
                                color=None,
                                asChain = False,
                                )

    arm = LocGuides.locGuides(
                                name='arm',
                                side='L',
                                size=1,
                                guideList=['arm%s' % i for i in range(3)],
                                color=None,
                                asChain=False,
                                mirror=True,
                                mirrorRotatoin=True,
                            )
    leg = LocGuides.locGuides(
                                name='leg',
                                side='L',
                                size=1,
                                guideList=['leg%s' % i for i in range(3)],
                                color=None,
                                asChain=False,
                                mirror=True,
                                mirrorRotatoin=True,
                            )

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