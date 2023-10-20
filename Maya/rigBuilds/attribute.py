import pymel.core as pm

"""
FUNCTION:      createTags
DESCRIPTION:   crates tags for easy selection
USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
RETURN:        None
REQUIRES:      None
Version        1.0.0
Examples:      SKIN     :   skinweights
               JOINTS   :   joints
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

"""
FUNCTION:      selectTags
DESCRIPTION:   select tags for easy selection
USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
RETURN:        List of of oject names as 
REQUIRES:      None
Version        1.0.0
"""

def selectTags(tagName='SKIN'):
    # list all objects with the specified tag attribute
    taggedObjs = []
    for node in pm.ls(type='transform'):
        if node.hasAttr(tagName):
            taggedObjs.append(node)
    if not taggedObjs:
        pm.warning('No objects found with the tag attribute: {}'.format(tagName))
    pm.select(taggedObjs)

    # return listed name as string
    strNameList = []
    for bah in taggedObjs:
        name = bah.name()
        strNameList.append(name)
    return strNameList


"""
FUNCTION:      toggleAttributeLock
DESCRIPTION:   lock and unlocks 
USAGE:         
RETURN:        None
REQUIRES:      None
Version        1.0.0
"""
def toggleAttributeLock(node='C_Control0_CNT', unlock=False):
    if not pm.objExists(node):
        return
    # If 'unlock' is False, we are in lock mode.
    if not unlock:
        attrs = ['visibility'] if pm.nodeType(node) == 'mesh' else pm.listAttr(node, k=True)

        if attrs:
            for attr in attrs:
                try:
                    pm.setAttr(f'{node}.{attr}', l=True, k=False)
                except:
                    continue
    # If 'unlock' is True, we are in unlock mode.
    else:
        attrs = pm.listAttr(node, l=1)

        if attrs:
            for attr in attrs:
                try:
                    pm.setAttr(f'{node}.{attr}', l=False, k=True)
                except:
                    continue