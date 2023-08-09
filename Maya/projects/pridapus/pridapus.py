import pymel.core as pm
import importlib as imp

from rigBuilds import LoadMaFile, BaseRig, LocGuidesIO, LocGuides, attribute, ControlMakerTools
imp.reload(LoadMaFile)
imp.reload(BaseRig)
imp.reload(LocGuides)
imp.reload(LocGuidesIO)
imp.reload(attribute)
imp.reload(ControlMakerTools)

from rigBuilds.rig import Spline
imp.reload(Spline)

# ControlMakerTools.scaleCurve(controlNames='C_global0_CNT', scale=2)
# ControlMakerTools.scaleCurve(controlNames='C_god0_CNT', scale=2)

# --- create locGuides
def createGuides():
    ControlMakerTools.scaleCurve(controlNames='C_global0_CNT', scale=2)
    ControlMakerTools.scaleCurve(controlNames='C_god0_CNT', scale=2)
    spine = LocGuides.locGuides(
                                name='spine',
                                side='C',
                                size=1,
                                nameList=['spine%s' % i for i in range(5)],
                                color=None,
                                )

    arm = LocGuides.locGuides(
                              name='arm',
                              side='L',
                              size=1,
                              nameList=['arm%s' % i for i in range(3)],
                              color=None,
                              mirror=True,
                              mirrorRotatoin=True,
                             )

    leg = LocGuides.locGuides(
                              name='leg',
                              side='L',
                              size=1,
                              nameList=['leg%s' % i for i in range(3)],
                              color=None,
                              mirror=True,
                              mirrorRotatoin=True,
                              )
 # --- create spline
def createRig():
    Spline.spline(side='C',
                  name='spline',
                  guideList=['C_spine%s_GDE' % i for i in range(5)],
                  numControls=3,
                  )

    

def cleanup():
    # this is cleanup phase to lock and hide things, and use ishistoricaly intersestiing
    pass

