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

def xspline(x, p1,p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    h = x2 - x1
    if h != 0:
        a = (- 2 * (y2 - y1)) / (h ** 3)
        b = (3 * (y2 - y1)) / (h ** 2)
        d = y1
        dx = x - x1
        y = a * dx ** 3 + b * dx ** 2 + d
    else:
        y = y1
    return y

def sort_2d_array(arr):
    if not arr:
        return arr
    sorted_arr = sorted(arr, key=lambda x: x[0])
    return sorted_arr

def interpolate_bezier(ratio, control_points):
    n = len(control_points) - 1

    def binomial_coefficient(i, n):
        """计算二项式系数"""
        from math import factorial
        return factorial(n) // (factorial(i) * factorial(n - i))

    def bernstein_poly(i, n, t):
        """计算Bernstein多项式"""
        return binomial_coefficient(i, n) * (1 - t)**(n - i) * t**i

    x, y, _ = zip(*control_points)
    z = [0] * (n + 1)

    point = [sum(bernstein_poly(i, n, ratio) * coord for i, coord in enumerate(axis)) for axis in [x, y, z]]

    return tuple(point)

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

def between_rows(x, matrix):
    if not matrix or not matrix[0]:
        return None

    # 获取数组的第一列
    first_column = [row[0] for row in matrix]

    # 寻找x在第一列中的位置
    index = 0
    while index < len(first_column) and x > first_column[index]:
        index += 1

    # 处理边界情况
    if index == 0:
        # x在第一行之前，返回第一行和第二行
        return matrix[0], matrix[1]
    elif index == len(first_column):
        # x在最后一行之后，返回倒数第二行和最后一行
        return matrix[-2], matrix[-1]
    else:
        # x在两行之间，返回相邻的两行
        return matrix[index - 1], matrix[index]

REMAP_TYPE_ID = om.MTypeId(0x0007f7f9)


CMPTCORE_TYPE_ID = om.MTypeId(0x0007f7a4)


class MBRemapNode(ommpx.MPxNode):
    TYPE_NAME = 'MBRemap'
    TYPE_ID = REMAP_TYPE_ID
    locator = None
    totalLocator = None
    totalIndex = None
    remapValue = None
    # test only
    count = None
    # init
    def __init__(self):
        super().__init__()

    @classmethod
    def creator(cls):
        return MBRemapNode()

    @classmethod
    def initialize(cls):
        numeric_attr = om.MFnNumericAttribute()

        #test only
        cls.count = numeric_attr.create('count', 'c', om.MFnNumericData.kInt)
        cls.addAttribute(cls.count)
        cls.totalLocator = numeric_attr.create('totalLocator', 'tl', om.MFnNumericData.kInt,4)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(4)
        cls.totalIndex = numeric_attr.create('totalIndex','tid',om.MFnNumericData.kInt,10)
        numeric_attr.setKeyable(True)
        numeric_attr.setMin(0)
        cls.locator = numeric_attr.create('locator','l',om.MFnNumericData.k3Double)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)


        cls.remapValue = numeric_attr.create('remapValue','v',om.MFnNumericData.kFloat)
        numeric_attr.setArray(True)
        numeric_attr.setUsesArrayDataBuilder(True)

        cls.addAttribute(cls.totalIndex)
        cls.addAttribute(cls.totalLocator)
        cls.addAttribute(cls.locator)
        cls.addAttribute(cls.remapValue)


        cls.attributeAffects(cls.totalIndex,cls.remapValue)
        cls.attributeAffects(cls.locator,cls.remapValue)
        cls.attributeAffects(cls.totalLocator,cls.remapValue)

        # test only
        cls.attributeAffects(cls.totalIndex, cls.count)
        cls.attributeAffects(cls.locator, cls.count)
        cls.attributeAffects(cls.totalLocator, cls.count)



    def compute(self, plug, data: om.MDataBlock):

        if plug == self.remapValue:
            totalIndex = data.inputValue(self.totalIndex).asInt()
            totalLocator = data.inputValue(self.totalLocator).asInt()
            remapValue_handle = data.outputArrayValue(self.remapValue)
            remapValue_builder = remapValue_handle.builder()
            locatorHandle = data.inputArrayValue(self.locator)
            pointList = []
            if locatorHandle.elementCount() >= totalLocator:
                for i in range(totalLocator):
                    locatorHandle.jumpToArrayElement(i)
                    locatorPoint = locatorHandle.inputValue().asDouble3()
                    pointList.append(locatorPoint)
            else:
                return
            pointList = sort_2d_array(pointList)


            for index in range(-totalIndex,totalIndex+1):
                x = (1.0*index/totalIndex)/2+0.5

                p1,p2 = between_rows(x,pointList)

                y = xspline(x, p1, p2)

                #output
                listIndex = indexToListIndex(index,totalIndex)
                remapValue_builder.addElement(listIndex).setFloat(y)

            remapValue_handle.setAllClean()
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

        cls.CVs = numeric_attr.create('CVs', 'cvs', om.MFnNumericData.kInt, 4)
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
        numeric_attr.setMin(0)
        numeric_attr.setMax(1)
        cls.addAttribute(cls.ratio)



        cls.iGuidePCG = numeric_attr.create('iGuidePCG', 'igpcg',om.MFnNumericData.k3Double)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)
        cls.addAttribute(cls.iGuidePCG)

        cls.iMiddlePCG = numeric_attr.create('iMiddlePCG', 'impcg', om.MFnNumericData.k3Double)
        numeric_attr.setKeyable(True)
        numeric_attr.setArray(True)
        cls.addAttribute(cls.iMiddlePCG)

        cls.oPCG = numeric_attr.create('oPCG', 'opcg', om.MFnNumericData.k3Double)
        numeric_attr.setArray(True)
        numeric_attr.setUsesArrayDataBuilder(True)
        cls.addAttribute(cls.oPCG)


        cls.attributeAffects(cls.iGuidePCG, cls.oPCG)
        cls.attributeAffects(cls.iMiddlePCG, cls.oPCG)
        cls.attributeAffects(cls.ratio, cls.oPCG)
        cls.attributeAffects(cls.totalIndex, cls.oPCG)
        cls.attributeAffects(cls.totalMiddles, cls.oPCG)
        cls.attributeAffects(cls.index, cls.oPCG)
        cls.attributeAffects(cls.CVs, cls.oPCG)




    #
    def compute(self,plug,data: om.MDataBlock):

        if plug == self.oPCG:
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
            if middleCVsCount >= totalMiddles * CVs:
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


            middleCGP = transpose_matrix(middleCGP)

            print(middleCGP)

            #output
            oPCG_handle = data.outputArrayValue(MBCmptCoreNode.oPCG)
            oPCG_builder = oPCG_handle.builder()
            for i,pointList in enumerate(middleCGP):
                # interpolate point here
                point = interpolate_bezier(ratio,pointList)
                x = point[0]
                y = point[1]
                oPCG_builder.addElement(i).set3Double(x,y,0)
            oPCG_handle.setAllClean()
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
