# TonysTools for Rigging
This is My own auto rigger That will be the base infrastructure for 
Any rigBuilds for Maya python 3.9

## TODO
fix ControlCurves joint in to parent

### #==== use in script editor Here ====
import pymel.core as pm

import sys
#### # this is to start up rigbuilds
sys.path.append('D:\OneDrive\TonyTools\Maya')
paths = sys.path
for i in paths:
    print(i)

import rigBuilds.startupRigBuilds as surb
surb.importingPaths() 

#### # this is to build the rig of the pridapus
import projects.pridapus.pridapusMain as work
reload(work)
#### # load base model
work.loadModel()

#### # ==== use in script editor Here ====