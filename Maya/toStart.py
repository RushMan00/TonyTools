# ===========================
'''
To start up my RigBuilds

copy and paste in to script editor

import sys
sys.path.append('/corp/home/tsong/Desktop/TonyTools')
# to print the list of sys.paths
paths = sys.path
for i in paths:
    print(i)

# import the test
import toStart as st
reload(st)
st.printThis()

'''

def printThis():
    print("tony's world is working!")


