import pymel.core as pm

def createTags(node='C_joint0_JNT', tagName='myTag', tagValue='myTagValue'):
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

def selectTags(tagName='SKIN'):
    """
    FUNCTION:      selectTags
    DESCRIPTION:   select tags for easy selection
    USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
    RETURN:        List of of oject names as
    REQUIRES:      None
    Version        1.0.0
    """
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



def toggleAttributeLock(node='C_Control0_CNT', unlock=False):
    """
    FUNCTION:      toggleAttributeLock
    DESCRIPTION:   lock and unlocks
    USAGE:         toggleAttributeLock(node='C_Control0_CNT', unlock=False)
    RETURN:        None
    REQUIRES:      None
    Version        1.0.0
    """
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

def checkAttributeExists(objectName, attributeName):
    """
    FUNCTION:      checkAttributeExists(object_name, attribute_name)
    DESCRIPTION:   Check if a specific attribute exists on a given object in Maya.
    USAGE:
    RETURN:        bool
    REQUIRES:      None
    Version        1.0.0
    """
    # Check if the object exists
    if pm.objExists(objectName):
        # Get the PyNode for the object
        obj = pm.PyNode(objectName)

        # Check if the attribute exists
        if obj.hasAttr(attributeName):
            return True, print('Yes, the attribute exists.')
        else:
            return False, print('No, the attribute does not exist.')
    else:
        print(f"The object '{objectName}' does not exist in the scene.")
