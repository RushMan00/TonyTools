import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm

def addAttrTitleSperator(nodeName='C_global0_CNT', attrName='Title'):
    # Adding an enum attribute to the specified node
    cmds.addAttr(nodeName, longName=attrName, attributeType='enum', enumName='Setup', keyable=True)
    cmds.setAttr(f'{nodeName}.{attrName}', e=1, lock=0, channelBox=0)
    return f'{nodeName}.{attrName}'


def addAttr(nodeName='C_global0_CNT', attrName='Title', attributeType='float',
            min=None, max=None, defaultValue=None, enumName=None):
    """
    FUNCTION:      addAttr
    DESCRIPTION:   Adds a new attribute of various types to a specified Maya node.
    USAGE:         addAttr(nodeName='C_global0_CNT', attrName='Title', attributeType='float',
                           min=None, max=None, defaultValue=None, enumName=None)
    RETURN:        str: The full path of the newly created attribute.
    REQUIRES:      None
    RAISES:        ValueError: If the node does not exist or if an unsupported attribute type is specified.
    Version        1.0.0
    
    """

    # Check if the specified node exists in the scene
    if not cmds.objExists(nodeName):
        raise ValueError(f"Node '{nodeName}' does not exist.")

    # Add an attribute based on its type
    if attributeType == 'enum':
        if not enumName:
            raise ValueError("enumName parameter must be provided for enum attributes.")
        cmds.addAttr(nodeName, longName=attrName, attributeType='enum', enumName=enumName, keyable=True)
    elif attributeType in ['float', 'double', 'int', 'long']:
        addAttrArgs = {
            'longName': attrName, 
            'attributeType': attributeType, 
            'keyable': True
        }
        if min is not None:
            addAttrArgs['min'] = min
        if max is not None:
            addAttrArgs['max'] = max
        if defaultValue is not None:
            addAttrArgs['defaultValue'] = defaultValue
        cmds.addAttr(nodeName, **addAttrArgs)
    else:
        # This can be extended to handle other attribute types
        raise ValueError(f"Unsupported attribute type: {attributeType}")

    # Unlock the attribute and make it visible in the channel box
    cmds.setAttr(f'{nodeName}.{attrName}', e=True, lock=False, 
                #  channelBox=False
                 )

    # Return the full path of the new attribute for further use
    return f'{nodeName}.{attrName}'


def createTags(nodeName='C_joint0_JNT', attrName= 'myTag', attrValue='myTagValue'):
    """
    FUNCTION:      createTags
    DESCRIPTION:   crates tags for easy selection
    USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
    RETURN:        String or None if object dont exist
    REQUIRES:      None
    Version        1.0.0
    Examples:      SKIN     :   skinweights'
                   JOINTS   :   joints
    """
    # check if the object exists
    if cmds.objExists(nodeName):
        # check if the attribute exists
        if not cmds.attributeQuery(attrName, node=nodeName, exists=True):
            # if it does not exist, create custom attrs
            cmds.addAttr(nodeName, longName=attrName, dataType='string')
            cmds.setAttr(f"{nodeName}.{attrName}", attrValue, type='string')
            print(f'added in new attribute on to {nodeName}.{attrName} with the attribute {attrValue}')
        return f"{nodeName}.{attrName}"

    else:
        cmds.warning(f'Object {nodeName} does not exist.')
        return None

def selectTags(tagName='SKIN'):
    """
    FUNCTION:      selectTags
    DESCRIPTION:   select tags for easy selection
    USAGE:         tagged_objs = pm.ls('*.*myTag' == 'myTagValue')
    RETURN:        List of object names as 'SKIN'
    REQUIRES:      None
    Version        1.0.0
    """

    # List all objects with the specified tag attribute
    allTransforms = cmds.ls(type='transform')
    taggedObjs = [obj for obj in allTransforms if cmds.attributeQuery(tagName, node=obj, exists=True)]

    if not taggedObjs:
        cmds.warning('No objects found with the tag attribute: {}'.format(tagName))

    # Select the tagged objects
    cmds.select(taggedObjs, replace=True)

    # Return the names of these objects
    return taggedObjs

def toggleAttributeLock(node='C_Control0_CNT', unlock=False):
    """
    FUNCTION:      toggleAttributeLock
    DESCRIPTION:   lock and unlocks
    USAGE:         toggleAttributeLock(node='C_Control0_CNT', unlock=False)
    RETURN:        None
    REQUIRES:      None
    Version        1.0.0
    """
    if not cmds.objExists(node):
        return

    # If 'unlock' is False, we are in lock mode.
    if not unlock:
        # Check if the node is a mesh and set attributes accordingly
        if cmds.nodeType(node) == 'mesh':
            attrs = ['visibility']
        else:
            attrs = cmds.listAttr(node, keyable=True)

        if attrs:
            for attr in attrs:
                try:
                    cmds.setAttr(f'{node}.{attr}', lock=True, keyable=False)
                except:
                    continue

    # If 'unlock' is True, we are in unlock mode.
    else:
        attrs = cmds.listAttr(node, locked=True)

        if attrs:
            for attr in attrs:
                try:
                    cmds.setAttr(f'{node}.{attr}', lock=False, keyable=True)
                except:
                    continue

def checkAttributeExists(node, attributeName):
    """
    FUNCTION:      checkAttributeExists(object_name, attribute_name)
    DESCRIPTION:   Check if a specific attribute exists on a given object in Maya.
    USAGE:
    RETURN:        bool
    REQUIRES:      None
    Version        1.0.0
    """
    # Check if the object exists
    if cmds.objExists(node):
        # Check if the attribute exists
        if cmds.attributeQuery(attributeName, node=node, exists=True):
            print('Yes, the attribute exists.')
            return True
        else:
            print('No, the attribute does not exist.')
            return False
    else:
        print(f"The object '{node}' does not exist in the scene.")

def getShapeNodes(nodeName='C_object_CNT'):
    """
    This function retrieves all the shape nodes under a given transform node using the OpenMaya API.

    Args:
    transformNodeName (str): The name of the transform node for which you want to retrieve the shape nodes.

    Returns:
    list: A list of strings, where each string is the name of a shape node under the given transform node.
    An empty list is returned if the node does not exist, is not a transform node, or if there are no shape nodes under it.

    Example Usage:
    shapeNodes = getShapeNodes('myTransformNode')
    print(shapeNodes)
    """
    # Check if the node exists
    # if list is less than one
    # else list iis more than one elements
    if not cmds.objExists(nodeName):
        print("Error: Node does not exist.")
        return []

    # Get the MObject for the given node
    selectionList = om.MSelectionList()
    selectionList.add(nodeName)
    node = om.MObject()
    selectionList.getDependNode(0, node)

    # Check if the MObject is a transform
    if not node.hasFn(om.MFn.kTransform):
        print("Error: Specified node is not a transform node.")
        return []

    # Get the shapes under the transform
    dagNode = om.MFnDagNode(node)
    shapeNames = []
    for i in range(dagNode.childCount()):
        child = dagNode.child(i)
        if child.hasFn(om.MFn.kShape):
            shapeFn = om.MFnDagNode(child)
            shapeName = shapeFn.name()
            shapeNames.append(shapeName)

    return shapeNames

