# TonysTools for Rigging
An auto rigger That will be the base infrastructure for 
Any rigBuilds for Maya python 3.9, that uses pymel as base.

works with Maya 2023

install pymel python package

Note to when building rigging system:

Matrix Rig Setup 
PROS: Fast in scene 
CONS: Dosn't work for games when baking animation for games
Solution: create both versions because why not?
ex. BipedMatrixRig())
ex. BipedRig()


### #==== use in script editor Here ====
import importlib as imp
import pymel.core as pm
import sys

### # --- start up rigbuilds 
### # import paths
sys.path.append('D:\OneDrive\TonyTools\Maya')
paths = sys.path
for i in paths:
    print(i)
import rigBuilds.startupRigBuilds as surb
surb.importingPaths() 

### # import projects
import projects.pridapus.pridapusMain as work
imp.reload(work)

### # --- UI concept
### # Load Model
imp.reload(work)
work.loadModel()
### # Locator Guides
imp.reload(work)
work.createGuildes()
### # LOAD Guide
imp.reload(work)
work.loadGuildes()  
### # SAVE Guide
imp.reload(work)
work.saveGuildes()    
### # Create Rig
imp.reload(work)
work.createRig()
### # tag Skinweights

### # save Skinweights
#### # ==== use in script editor Here ====