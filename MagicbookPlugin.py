from random import random
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import maya.cmds as cmds

def calculate_spline(x, x1, x2, y1, y2, dydx1=0, dydx2=0):
    h = x2 - x1
    if h != 0:
        a = (dydx1 + dydx2 - 2 * (y2 - y1) / h) / (h * h)
        b = (3 * (y2 - y1) / h - 2 * dydx1 - dydx2) / h
        c = dydx1
        d = y1
        dx = x - x1
        y = a * dx ** 3 + b * dx ** 2 + c * dx + d
    else:
        y=y1
    return y



def linear(x,x1,x2,y1,y2):
    y = y1+(y2-y1)*(x-x1)/(x2-x1)
    return y

class MBRemapNode(ommpx.MPxNode):
    TYPE_NAME = 'MBRemap'
    TYPE_ID = om.MTypeId(0x0007f7f1)

    x0 = None
    x1 = None
    x2 = None
    x3 = None
    y0 = None
    y1 = None
    y2 = None
    y3 = None
    projection = None
    index = None
    totalIndex = None

    # init
    def __init__(self):
        super().__init__()

    @classmethod
    def creator(cls):
        return MBRemapNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.x0 = numeric_attr.create('x0', 'x0', om.MFnNumericData.kFloat, 0.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.y0 = numeric_attr.create('y0', 'y0', om.MFnNumericData.kFloat, 0.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.x1 = numeric_attr.create('x1', 'x1', om.MFnNumericData.kFloat, 0.25)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.y1 = numeric_attr.create('y1', 'y1', om.MFnNumericData.kFloat, 0.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.x2 = numeric_attr.create('x2', 'x2', om.MFnNumericData.kFloat, 0.75)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.y2 = numeric_attr.create('y2', 'y2', om.MFnNumericData.kFloat, 1.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.x3 = numeric_attr.create('x3', 'x3', om.MFnNumericData.kFloat, 1.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.y3 = numeric_attr.create('y3', 'y3', om.MFnNumericData.kFloat, 1.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0.0)
        numeric_attr.setMax(1.0)
        cls.addAttribute(cls.x0)
        cls.addAttribute(cls.x1)
        cls.addAttribute(cls.x2)
        cls.addAttribute(cls.x3)
        cls.addAttribute(cls.y0)
        cls.addAttribute(cls.y1)
        cls.addAttribute(cls.y2)
        cls.addAttribute(cls.y3)

        cls.totalIndex = numeric_attr.create('totalIndex', 'tid', om.MFnNumericData.kInt, 0)
        cls.addAttribute(cls.totalIndex)

        cls.index = numeric_attr.create('index', 'id', om.MFnNumericData.kFloat, 0.0)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)
        numeric_attr.setReadable(True)
        numeric_attr.setUsesArrayDataBuilder(True)
        numeric_attr.setIndexMatters(False)
        cls.addAttribute(cls.index)

        cls.projection = numeric_attr.create('projection', 'prj', om.MFnNumericData.kFloat, 0.0)
        # numeric_attr.setKeyable(True)!!!!!!!!!!!!!!!!!!NOT GOING TO WORK!!!!!!!!
        # numeric_attr.setHidden(False)
        numeric_attr.setArray(True)
        numeric_attr.setReadable(True)
        numeric_attr.setWritable(False)
        numeric_attr.setUsesArrayDataBuilder(True)
        # numeric_attr.setIndexMatters(False)
        cls.addAttribute(cls.projection)

        # Affects

        cls.attributeAffects(cls.index, cls.totalIndex)
        # cls.attributeAffects(cls.totalIndex, cls.totalIndex)
        # print(cls.projection)
        cls.attributeAffects(cls.index, cls.projection)
        #
        cls.attributeAffects(cls.x0, cls.projection)
        cls.attributeAffects(cls.x1, cls.projection)
        cls.attributeAffects(cls.x2, cls.projection)
        cls.attributeAffects(cls.x3, cls.projection)

        cls.attributeAffects(cls.y0, cls.projection)
        cls.attributeAffects(cls.y1, cls.projection)
        cls.attributeAffects(cls.y2, cls.projection)
        cls.attributeAffects(cls.y3, cls.projection)



    def compute(self, plug, data: om.MDataBlock):
        indexArrayDataHandle = data.inputArrayValue(MBRemapNode.index)
        totalIndex = indexArrayDataHandle.elementCount()
        data.outputValue(MBRemapNode.totalIndex).setInt(totalIndex)

        projectionArrayDataHandle = data.outputArrayValue(MBRemapNode.projection)
        projectionArrayDataBuilder = projectionArrayDataHandle.builder()

        x0 = data.inputValue(MBRemapNode.x0).asFloat()
        x1 = data.inputValue(MBRemapNode.x1).asFloat()
        x2 = data.inputValue(MBRemapNode.x2).asFloat()
        x3 = data.inputValue(MBRemapNode.x3).asFloat()
        y0 = data.inputValue(MBRemapNode.y0).asFloat()
        y1 = data.inputValue(MBRemapNode.y1).asFloat()
        y2 = data.inputValue(MBRemapNode.y2).asFloat()
        y3 = data.inputValue(MBRemapNode.y3).asFloat()

        for i in range(totalIndex):
            # get input
            indexArrayDataHandle.jumpToElement(i)
            x = indexArrayDataHandle.inputValue().asFloat()
            # calculate

            if(x>=x0 and x<x1):
                y = calculate_spline(x, x0, x1, y0, y1)
            elif (x >= x1 and x < x2):
                y = calculate_spline(x, x1, x2, y1, y2)
            else:
                y = calculate_spline(x, x2, x3, y2, y3)

            # output

            projectionDataHandle = projectionArrayDataBuilder.addElement(i)
            projectionDataHandle.setFloat(y)

        data.setClean(plug)


def initializePlugin(plugin):
    vendor = "OtakuSquirrel"
    version = "2.0.0"
    plugin_fn = ommpx.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerNode(MBRemapNode.TYPE_NAME,
                               MBRemapNode.TYPE_ID,
                               MBRemapNode.creator,
                               MBRemapNode.initialize,
                               ommpx.MPxNode.kDependNode)
        om.MGlobal.displayInfo("initialized:{0}".format(MBRemapNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to initialize:{0}".format(MBRemapNode.TYPE_NAME))


def uninitializePlugin(plugin):
    plugin_fn = ommpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(MBRemapNode.TYPE_ID)
        om.MGlobal.displayInfo("uninitialized:{0}".format(MBRemapNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to uninitialized:{0}".format(MBRemapNode.TYPE_NAME))


if __name__ == "__main__":
    plugin_name = 'MagicbookPlugin.py'
    cmds.file(new=True, force=True)
    print('new file:#', int(random() * 10000), '#')
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
