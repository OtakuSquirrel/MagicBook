from random import random
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommpx
import maya.cmds as cmds
import math

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
        y = y1
    return y

def catmull_rom_interpolation(p0, p1, p2, p3, t):
    """
    Catmull-Rom 插值函数
    """
    return (
        0.5 * ((2 * p1) +
               (-p0 + p2) * t +
               (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 +
               (-p0 + 3 * p1 - 3 * p2 + p3) * t**3)
    )

def interpolate_point(ratio, point_list):
    """
    使用 Catmull-Rom 样条曲线插值计算指定比例下的点
    """
    num_points = len(point_list)
    if num_points < 4:
        raise ValueError("需要至少4个点来执行 Catmull-Rom 插值。")

    # 确保 ratio 在 0 到 1 之间
    ratio = max(0.0, min(ratio, 1.0))

    # 计算 ratio 对应的索引
    t = ratio * (num_points - 1)

    # 获取四个相邻的点
    i0 = int(t)
    i1 = min(i0 + 1, num_points - 1)
    i2 = min(i0 + 2, num_points - 1)
    i3 = min(i0 + 3, num_points - 1)

    # 获取相邻的四个点
    p0 = point_list[i0]
    p1 = point_list[i1]
    p2 = point_list[i2]
    p3 = point_list[i3]

    # 计算插值
    interpolated_point = catmull_rom_interpolation(p0, p1, p2, p3, t - i0)

    return interpolated_point



def linear(x, x1, x2, y1, y2):
    y = y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return y

def transpose_matrix(matrix):
    """
    将二维数组的行和列进行转置
    """
    return [list(row) for row in zip(*matrix)]

def findPos(x,columns):
    if columns:
        t = x/columns
    else:
        t = 0
    quotient = math.floor(t)
    remainder = x-columns*quotient
    return quotient,remainder

def has_none_value(arr):
    if isinstance(arr, list):
        for element in arr:
            if has_none_value(element):
                return True
    else:
        return arr is None

def indexToListIndex(index, totalIndex):
    return index + totalIndex



def listIndexToIndex(listIndex, totalIndex):
    return listIndex - totalIndex


def blendList(ratio, list0, list1):
    outputList = []
    for item0, item1 in zip(list0, list1):
        cv = item0 * (1 - ratio) + item1 * ratio
        outputList.append(cv)
    return outputList

def blendListList(ratio,listList0,listList1):
    outputList = []
    for list0,list1 in zip(listList0, listList1):
        midList = blendList(ratio,list0,list1)
        outputList.append(midList)
    return outputList

def interpolation(ratio, PCGs0, PCGs1):
    outputList = []
    cvsMaxIndex = len(PCGs0[0])
    gap = 1.0 / cvsMaxIndex
    section = int(ratio // gap)
    if ratio == 1:
        section = section - 1
    ratio_fix = (ratio % gap) / gap
    PCG0 = PCGs0[section]
    PCG1 = PCGs1[section]

    for item0, item1 in zip(PCG0, PCG1):
        outputList.append(blendList(ratio_fix, item0, item1))
    # output a list of pos look like:[[0,0],[1,1],[2,2],[3,3]]
    return outputList

REMAP_TYPE_ID = om.MTypeId(0x0007f7f1)


CMPTCORE_TYPE_ID = om.MTypeId(0x0007f7a4)


class MBRemapNode(ommpx.MPxNode):
    TYPE_NAME = 'MBRemap'
    TYPE_ID = REMAP_TYPE_ID
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
            if (x >= x0 and x < x1):
                y = calculate_spline(x, x0, x1, y0, y1)
            elif (x >= x1 and x < x2):
                y = calculate_spline(x, x1, x2, y1, y2)
            else:
                y = calculate_spline(x, x2, x3, y2, y3)

            # output

            projectionDataHandle = projectionArrayDataBuilder.addElement(i)
            projectionDataHandle.setFloat(y)

        data.setClean(plug)


class MBCmptCoreNode(ommpx.MPxNode):
    TYPE_NAME = 'MBCmptCore'
    TYPE_ID = CMPTCORE_TYPE_ID
    # INPUT
    iGuidePCG = None
    iMiddlePCG = None
    CVs = None
    totalMiddles = None
    totalIndex = None
    index = None
    ratio = None

    # OUTPUT
    oPCG = None
    oMessage = None

    def __init__(self):
        super().__init__()

    @classmethod
    def creator(cls):
        return MBCmptCoreNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        cls.CVs = numeric_attr.create('CVs', 'cvs', om.MFnNumericData.kInt, 5)
        numeric_attr.setKeyable(True)
        cls.addAttribute(cls.CVs)

        cls.totalMiddles = numeric_attr.create('totalMiddles', 'tm', om.MFnNumericData.kInt, 3)
        numeric_attr.setKeyable(True)
        cls.addAttribute(cls.totalMiddles)

        cls.totalIndex = numeric_attr.create('totalIndex', 'tid', om.MFnNumericData.kInt, 10)
        numeric_attr.setKeyable(True)
        cls.addAttribute(cls.totalIndex)

        cls.index = numeric_attr.create('index', 'i', om.MFnNumericData.kInt, 0)
        numeric_attr.setKeyable(True)
        cls.addAttribute(cls.index)

        cls.ratio = numeric_attr.create('ratio', 'r', om.MFnNumericData.kDouble, 0.5)
        numeric_attr.setKeyable(True)
        cls.addAttribute(cls.ratio)



        # test only
        cls.oMessage = numeric_attr.create('oMessage','om',om.MFnNumericData.kInt,0)
        cls.addAttribute(cls.oMessage)

        cls.iGuidePCG = numeric_attr.create('iGuidePCG', 'igpcg',om.MFnNumericData.k3Double)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)
        # numeric_attr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.iGuidePCG)

        cls.iMiddlePCG = numeric_attr.create('iMiddlePCG', 'impcg', om.MFnNumericData.k3Double)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)
        numeric_attr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.iMiddlePCG)

        cls.oPCG = numeric_attr.create('oPCG', 'opcg', om.MFnNumericData.k3Double)
        numeric_attr.setArray(True)
        numeric_attr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.oPCG)

        cls.attributeAffects(cls.iGuidePCG, cls.oPCG)
        cls.attributeAffects(cls.iMiddlePCG, cls.oPCG)
        cls.attributeAffects(cls.ratio, cls.oPCG)
        cls.attributeAffects(cls.totalIndex, cls.oPCG)
        cls.attributeAffects(cls.index, cls.oPCG)

        # test only
        cls.attributeAffects(cls.iGuidePCG, cls.oMessage)
        cls.attributeAffects(cls.iMiddlePCG, cls.oMessage)
        cls.attributeAffects(cls.ratio, cls.oMessage)
        cls.attributeAffects(cls.totalIndex, cls.oMessage)
        cls.attributeAffects(cls.index, cls.oMessage)
        cls.attributeAffects(cls.CVs, cls.oMessage)



    #
    def compute(self,plug,data: om.MDataBlock):
        # test only
        oMessage = data.outputValue(self.oMessage)

        #
        index = data.inputValue(self.index).asInt()
        ratio = data.inputValue(self.ratio).asDouble()
        CVs = data.inputValue(self.CVs).asInt()
        totalIndex = data.inputValue(self.totalIndex).asInt()
        totalMiddles = data.inputValue(self.totalMiddles).asInt()

        iGuidePCG = data.inputArrayValue(self.iGuidePCG)
        iMiddlePCG = data.inputArrayValue(self.iMiddlePCG)
        #
        limitRatio = 0.5
        if totalIndex != 0:
            limitRatio = (1.0*index/totalIndex)/2+0.5
        #
        columns = CVs
        rows = 4

        guideCVsCount = iGuidePCG.elementCount()
        if guideCVsCount >= 4 * CVs:
            guideCGP = [[None] * columns for _ in range(rows)]
            for i in range(4 * CVs):
                row, column = findPos(i, CVs)
                iGuidePCG.jumpToArrayElement(i)
                currentValue = iGuidePCG.inputValue().asDouble3()
                guideCGP[row][column] = list(currentValue)

            guideLCGP = blendListList(limitRatio,guideCGP[0],guideCGP[1])
            guideRCGP = blendListList(limitRatio, guideCGP[2], guideCGP[3])

        else:
            return

        middleCVsCount = iMiddlePCG.elementCount()
        if middleCVsCount == totalMiddles * CVs:
            rows = totalMiddles
            middleCGP = [[None] * columns for _ in range(rows)]
            for i in range(totalMiddles * CVs):
                row, column = findPos(i, CVs)
                iGuidePCG.jumpToArrayElement(i)
                currentValue = iGuidePCG.inputValue().asDouble3()
                middleCGP[row][column] = list(currentValue)

        else:
            return
        middleCGP.insert(0, guideLCGP)
        middleCGP.append(guideRCGP)

        print(middleCGP)

        middleCGP = transpose_matrix(middleCGP)

        finalCGP = []
        for pointList in middleCGP:


        # test only
        oMessage.setInt(guideCVsCount)
        data.setClean(plug)



def initializePlugin(plugin):
    vendor = "OtakuSquirrel"
    version = "2.0.0"
    plugin_fn = ommpx.MFnPlugin(plugin, vendor, version)
    # register remapNode
    try:
        plugin_fn.registerNode(MBRemapNode.TYPE_NAME,
                               MBRemapNode.TYPE_ID,
                               MBRemapNode.creator,
                               MBRemapNode.initialize,
                               ommpx.MPxNode.kDependNode)
        om.MGlobal.displayInfo("initialized:{0}".format(MBRemapNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to initialize:{0}".format(MBRemapNode.TYPE_NAME))

    # register cmptCore
    try:
        plugin_fn.registerNode(MBCmptCoreNode.TYPE_NAME,
                               MBCmptCoreNode.TYPE_ID,
                               MBCmptCoreNode.creator,
                               MBCmptCoreNode.initialize,
                               ommpx.MPxNode.kDependNode)
        om.MGlobal.displayInfo("initialized:{0}".format(MBCmptCoreNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to initialize:{0}".format(MBCmptCoreNode.TYPE_NAME))

def uninitializePlugin(plugin):
    plugin_fn = ommpx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterNode(MBRemapNode.TYPE_ID)
        om.MGlobal.displayInfo("uninitialized:{0}".format(MBRemapNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to uninitialized:{0}".format(MBRemapNode.TYPE_NAME))

    try:
        plugin_fn.deregisterNode(MBCmptCoreNode.TYPE_ID)
        om.MGlobal.displayInfo("uninitialized:{0}".format(MBCmptCoreNode.TYPE_NAME))
    except:
        om.MGlobal.displayInfo("fail to uninitialized:{0}".format(MBCmptCoreNode.TYPE_NAME))


if __name__ == "__main__":
    plugin_name = 'MagicBookPlugin.py'
    cmds.file(new=True, force=True)
    print('new file:#', int(random() * 10000), '#')
    cmds.evalDeferred('if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(plugin_name))
    cmds.evalDeferred('if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(plugin_name))
