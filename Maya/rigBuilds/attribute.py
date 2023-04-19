import pymel.core as pm

"""
__________________________________________________
FUNCTION:      createTags
DESCRIPTION:   crates tags for easy selection
USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
RETURN:        None
REQUIRES:      None
Version        1.0.0
__________________________________________________
"""

def createTags(node='C_joint0_JNT', tagName='myTag', tagValue='myTagValue'):
    # check if the object exists
    if pm.objExists(node):
        # get the PyNode object
        obj = pm.PyNode(node)
        # add the custom attribute
        obj.addAttr(tagName, dataType='string')
        # set the value of the attribute
        obj.attr(tagName).set(tagValue)
    else:
        pm.warning('Object ' + node + ' does not exist.')