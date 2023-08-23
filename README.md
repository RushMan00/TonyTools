# TonysTools for Rigging: Streamlining Production with Maya
Welcome to the TonysTools for Rigging repository—a dedicated solution 
crafted to revolutionize rigging systems in a production pipeline.
Designed exclusively for use with Maya 2023, our innovative toolkit aims 
to propel your rigging workflows to new heights. Whether you're a 
seasoned rigger or a curious newcomer, this repository is your gateway 
to optimized efficiency, enhanced collaboration, and top-tier results.

In this README, we'll delve into the core features, installation 
guidelines, and how you can integrate TonysTools seamlessly into 
your rigging process. Let's embark on a journey to unlock the full 
potential of rigging within a production environment.


###  how to start up rigbuilds
import pymel.core as pm

import maya.cmds as cmds

import importlib as imp

import sys

import paths

`sys.path.append('D:\OneDrive\TonyTools\Maya')
paths = sys.path
for i in paths:
    print(i)`
#### import more paths and other things
`import rigBuilds.startupRigBuilds as surb
surb.importingPaths()`


### Note to self
Matrix Rig Setup 
PROS: Fast in scene 
CONS: Dosn't work for games when baking animation for games
Solution: create both versions because why not?
ex. BipedMatrixRig())
ex. BipedRig()
