import maya.cmds as cmds
import os

# Name
def indexToID(index):
    if index >= 0:
        ID = 'P' + str(index)
    else:
        ID = 'N' + str(abs(index))
    return ID


def IDToIndex(ID):
    if ID[0] == 'P':
        index = int(ID[1:])
    elif ID[0] == 'N':
        index = -1 * int(ID[1:])
    else:
        return 0
    return index


def iToShaderName(i):
    return f'MB_S_Ramp_{i}'


def IDToShaderID(ID):
    return f'MB_S_' + ID


def indexToMeshName(index):
    meshName = 'MB_Mesh_' + indexToID(index)
    return meshName


def indexToMeshShapeName(index):
    meshShapeName = 'MB_Mesh_' + indexToID(index) + 'Shape'
    return meshShapeName


def IDToMeshName(ID):
    meshName = 'MB_Mesh_' + ID
    return meshName


def IDToMeshShapeNode(ID):
    return 'MB_Mesh_' + ID + 'Shape'


def meshNameToIndex(meshName):
    ID = meshName[8:]
    index = IDToIndex(ID)
    return index


def meshNameToID(meshName):
    return meshName[8:]


def indexToJntName(index):
    return 'MB_Jnt_' + indexToID(index)


def IDToJntName(ID):
    return 'MB_Jnt_' + ID


def jntNameToIndex(jntName):
    return IDToIndex(jntName[8:])


def jntNameToID(jntName):
    return jntName[8:]


def addSuffix(name, i):
    return name + '_' + str(i)


def indexToSkinClusterName(index):
    return 'MB_SkinCluster_' + indexToID(index)


def IDToSkinClusterName(ID):
    return 'MB_SkinCluster_' + ID


def skinClusterNameToIndex(skinClusterName):
    return IDToIndex(skinClusterName[15:])


def skinClusterNameToID(skinClusterName):
    return skinClusterName[15:]


def indexToCrvName(index):
    return 'MB_Crv_' + indexToID(index)


def IDToCrvName(ID):
    return 'MB_Crv_' + ID


def IDToCrvShapeName(ID):
    return 'MB_Crv_Shape_' + ID


def crvNameToIndex(crvName):
    return IDToIndex(crvName[8:])


def crvNameToID(crvName):
    return crvName[8:]


def indexToIKHandleName(index):
    return 'MB_IKHandle_' + indexToID(index)


def IDToIKHandleName(ID):
    return 'MB_IKHandle_' + ID


def IKHandleNameToIndex(ikhandleName):
    return IDToIndex(ikhandleName[12:])


def IKHandleNameToID(ikhandleName):
    return ikhandleName[12:]


def IDToControlerName(ID):
    return 'MB_Controller_' + ID


def controlerNameToID(controlerName):
    return controlerName[10:]


def IDToBSName(ID):
    return 'MB_BS_' + ID


def indexToBSName(index):
    ID = indexToID(index)
    return IDToBSName(ID)


def IDToCmptCore(ID):
    return 'MB_CmptCore_' + ID


def indexToMiddleIDs(totalMiddles):
    return [f'Mid{id}' for id in range(totalMiddles)]


def BSIDToIndex(BSID):
    return int(BSID[2:])


def IDToPointOnCurve(ID):
    return 'MB_PointOnCurve_' + ID


def totalBSsToBSIDs(totalBSs):
    return [f'BS{i}' for i in range(totalBSs)]


def totalBSsToRemapIDs(totalBSs):
    return [f'MB_Remap_BS{i}' for i in range(totalBSs)]


def IDToRemapID(ID):
    return 'MB_Remap_' + ID


def IDToRemapControllerLoc(ID):
    return f'Loc_{ID}'


# Create Rig
def indexRange(totalIndex):
    return range(-1 * totalIndex, totalIndex + 1)


def createMBShader(colorList):
    rampfix = []
    for i in colorList:
        tubfix = [x / 255 for x in i]
        rampfix.append(tubfix)
    for index in range(len(colorList)):
        shaderBallName = f'MB_S_Ramp_{index}'
        deleteIfExist(shaderBallName)
        MB_S_Ramp = cmds.shadingNode('blinn', asShader=True, name=shaderBallName)
        cmds.setAttr(MB_S_Ramp + '.color', rampfix[index][0], rampfix[index][1], rampfix[index][2], type='double3')
        cmds.setAttr(MB_S_Ramp + '.transparency', 0.3, 0.3, 0.3, type='double3')


def deleteIfExist(name):
    if cmds.objExists(name):
        cmds.delete(name)


def getJntPosList(width, subDivWidth):
    jntPosList = []
    for i in range(subDivWidth + 1):
        y = i * width / subDivWidth
        pos = (0, y, 0)
        jntPosList.append(pos)

    return jntPosList


def getCVsPosList(cvsMaxIndex, width):
    cvsList = []
    interval = width / (cvsMaxIndex - 1)

    for i in range(cvsMaxIndex):
        y = interval * i
        pos = (0, y, 0)
        cvsList.append(pos)

    return cvsList


def createRigTree():
    cmds.select(clear=True)
    levelName = 'MagicBookGrp'
    parentName = None
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'Main'
    parentName = 'MagicBookGrp'
    deleteIfExist(levelName)
    cmds.circle(n=levelName, normal=[0, 1, 0], radius=10)
    # cmds.addAttr()
    cmds.parent(levelName, parentName)

    levelName = 'PageGeo'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('PageGeo.inheritsTransform', False)

    levelName = 'GuideGeo'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('GuideGeo.inheritsTransform', False)

    levelName = 'PagesCurveGrp'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('PagesCurveGrp.v', False)

    levelName = 'GuideCurveGrp'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'BookSpine'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'RemapController'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'BSGrp'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'DeformationSystem'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'IKHandleGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('IKHandleGrp.v', False)

    levelName = 'JntGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('JntGrp.v', False)


def createMesh(ID, width, height, subDivWidth, subDivHeight):
    cmds.select(clear=True)
    meshName = IDToMeshName(ID)
    deleteIfExist(meshName)
    mesh = cmds.polyPlane(name=meshName, w=width, h=height, sw=subDivWidth, sh=subDivHeight)
    plugHandle = '.rotatePivotX'
    cmds.setAttr(meshName + plugHandle, -width / 2)
    plugHandle = '.tx'
    cmds.setAttr(meshName + plugHandle, width / 2)
    plugHandle = '.rz'
    cmds.setAttr(meshName + plugHandle, 90)
    cmds.makeIdentity(mesh, apply=True, rotate=True, scale=True, translate=True)
    cmds.delete(constructionHistory=True)

    cmds.parent(meshName, 'PageGeo')


def createJointChain(ID, width, subDivWidth):
    cmds.select('JntGrp')
    jntName = IDToJntName(ID)
    jntPosList = getJntPosList(width, subDivWidth)
    for jntIndex in range(len(jntPosList)):
        jntNameSuffix = addSuffix(jntName, jntIndex)
        jntPos = jntPosList[jntIndex]
        deleteIfExist(jntNameSuffix)
        cmds.joint(n=jntNameSuffix, p=jntPos, radius=0.1)


def bindSkin(ID):
    meshName = IDToMeshName(ID)
    jntName = IDToJntName(ID)
    jntName = addSuffix(jntName, 0)
    skinClusterName = IDToSkinClusterName(ID)
    deleteIfExist(skinClusterName)
    cmds.skinCluster(jntName, meshName, name=skinClusterName)
    cmds.setAttr(f'{meshName}.tx', lock=False)
    cmds.setAttr(f'{meshName}.ty', lock=False)
    cmds.setAttr(f'{meshName}.tz', lock=False)
    cmds.setAttr(f'{meshName}.sx', lock=False)
    cmds.setAttr(f'{meshName}.sy', lock=False)
    cmds.setAttr(f'{meshName}.sz', lock=False)


def injectJntWeight(ID, subDivWidth, subDivHeight):
    skinClusterName = IDToSkinClusterName(ID)
    weightListHandle = '.weightList'
    weightsHandle = '.weights'
    totalJntIndex = subDivWidth + 1
    totalPointIndex = (subDivWidth + 1) * (subDivHeight + 1)
    for point in range(totalPointIndex):
        column = point % (subDivWidth + 1)
        for joint in range(totalJntIndex):
            attributeName = f'{skinClusterName}{weightListHandle}[{point}]{weightsHandle}[{joint}]'
            if joint == column:
                cmds.setAttr(attributeName, 1.0)
            else:
                cmds.setAttr(attributeName, 0.0)


def createCVCurve(ID, width, cvsMaxIndex=4):
    cmds.select(clear=True)
    crvName = IDToCrvName(ID)
    deleteIfExist(crvName)
    cvsList = getCVsPosList(cvsMaxIndex, width)
    cmds.curve(name=crvName, p=cvsList)
    cmds.parent(crvName, 'PagesCurveGrp')
    children = cmds.listRelatives(crvName, children=True, fullPath=False)
    crvShapeName = IDToCrvShapeName(ID)
    cmds.rename(children[0], crvShapeName)
    cmds.hide(crvShapeName)


def createIKHandle(ID, subDivWidth):
    cmds.select(clear=True)
    ikHandleName = IDToIKHandleName(ID)
    curveName = IDToCrvName(ID)
    jointName = IDToJntName(ID)
    jointStart = addSuffix(jointName, 0)
    jointEnd = addSuffix(jointName, subDivWidth)
    deleteIfExist(ikHandleName)
    cmds.ikHandle(name=ikHandleName, startJoint=jointStart, endEffector=jointEnd, createCurve=False,
                  curve=curveName, solver='ikSplineSolver', parentCurve=False)
    cmds.parent(ikHandleName, 'IKHandleGrp')
    cmds.hide(ikHandleName)


def createController(ID, width, cvsMaxIndex=4):
    controlerName = IDToControlerName(ID)
    curveName = IDToCrvName(ID)
    curveShapeName = IDToCrvShapeName(ID)
    cvsList = getCVsPosList(cvsMaxIndex, width)
    for i in range(cvsMaxIndex):
        controlerName_suffix = controlerName + '_' + str(i)
        cmds.createNode('joint', name=controlerName_suffix)
        plugHandle = '.tx'
        cmds.setAttr(controlerName_suffix + plugHandle, cvsList[i][0])
        plugHandle = '.ty'
        cmds.setAttr(controlerName_suffix + plugHandle, cvsList[i][1])
        plugHandle = '.tz'
        cmds.setAttr(controlerName_suffix + plugHandle, cvsList[i][2])
        plugHandle = '.rz'
        cmds.setAttr(controlerName_suffix + plugHandle, 90)
        cmds.makeIdentity(controlerName_suffix, apply=True, rotate=True, scale=True, translate=False)
        cmds.parent(controlerName_suffix, curveName)
        cmds.delete(constructionHistory=True)
        shapeNodePlug = f'.controlPoints[{i}]'

        plugHandle = '.tx'
        dsPlugHandle = '.xValue'

        cmds.connectAttr(controlerName_suffix + plugHandle, curveShapeName + shapeNodePlug + dsPlugHandle)

        plugHandle = '.ty'
        dsPlugHandle = '.yValue'
        cmds.connectAttr(controlerName_suffix + plugHandle, curveShapeName + shapeNodePlug + dsPlugHandle)

        plugHandle = '.tz'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True)
        plugHandle = '.rx'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.ry'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.rz'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sx'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sy'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.sz'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        plugHandle = '.v'
        cmds.setAttr(controlerName_suffix + plugHandle, lock=True, keyable=False, channelBox=False)
        try:
            cmds.setAttr(f'{controlerName_suffix}.overrideEnabled', True)
            cmds.setAttr(f'{controlerName_suffix}.overrideColor', i + 14)
        except:
            pass


def createGuides(width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    guideIDs = ['LL', 'LR', 'RL', 'RR']

    for i in range(len(guideIDs)):
        if i < 2:
            shaderName = iToShaderName(4)
        else:
            shaderName = iToShaderName(5)
        ID = guideIDs[i]
        createMesh(ID, width, height, subDivWidth, subDivHeight)
        cmds.parent(IDToMeshName(ID), 'GuideGeo')
        cmds.hyperShade(assign=shaderName)
        createJointChain(ID, width, subDivWidth)
        bindSkin(ID)
        injectJntWeight(ID, subDivWidth, subDivHeight)
        createCVCurve(ID, width, cvsMaxIndex)
        crvName = IDToCrvName(ID)
        cmds.parent(crvName, 'GuideCurveGrp')
        createIKHandle(ID, subDivWidth)
        createController(ID, width, cvsMaxIndex)


def createMiddles(totalMiddles, width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    MiddleIDs = indexToMiddleIDs(totalMiddles)
    shaderName = iToShaderName(6)
    for i in range(len(MiddleIDs)):
        ID = MiddleIDs[i]
        createMesh(ID, width, height, subDivWidth, subDivHeight)
        cmds.parent(IDToMeshName(ID), 'GuideGeo')
        cmds.hyperShade(assign=shaderName)
        createJointChain(ID, width, subDivWidth)
        bindSkin(ID)
        injectJntWeight(ID, subDivWidth, subDivHeight)
        createCVCurve(ID, width, cvsMaxIndex)
        crvName = IDToCrvName(ID)
        cmds.parent(crvName, 'GuideCurveGrp')
        createIKHandle(ID, subDivWidth)
        createController(ID, width, cvsMaxIndex)


def createPage(ID, width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    createMesh(ID, width, height, subDivWidth, subDivHeight)
    createJointChain(ID, width, subDivWidth)
    bindSkin(ID)
    injectJntWeight(ID, subDivWidth, subDivHeight)
    createCVCurve(ID, width, cvsMaxIndex)
    createIKHandle(ID, subDivWidth)
    createController(ID, width, cvsMaxIndex)


def createBSTarget(BSIDs, width, height, subDivWidth, subDivHeight):
    shaderName = iToShaderName(7)
    for i, BSID in enumerate(BSIDs):
        createMesh(BSID, width, height, subDivWidth, subDivHeight)
        BSName = IDToMeshName(BSID)

        bend0 = cmds.nonLinear(type='bend', curvature=0, n=f'{BSName}_Bend_0', lowBound=0)
        bend0Handle = f'{BSName}_Bend_0Handle'
        cmds.setAttr(f'{bend0Handle}.rx', -45)
        cmds.select(BSName)
        bend1 = cmds.nonLinear(type='bend', curvature=0, n=f'{BSName}_Bend_1', lowBound=0)
        bend1Handle = f'{BSName}_Bend_1Handle'
        cmds.setAttr(f'{bend1Handle}.rx', 45)

        cmds.select(BSName)
        cmds.hyperShade(assign=shaderName)
        cmds.parent(bend0Handle, BSName)
        cmds.parent(bend1Handle, BSName)
        cmds.parent(BSName, 'BSGrp')
        cmds.setAttr(f'{BSName}.tx', i * -3)
    cmds.setAttr('BSGrp.tx', -20)


def conductBS(BSIDs, ID):
    for BSID in BSIDs:
        pageName = IDToMeshName(ID)
        BSTargetName = IDToMeshShapeNode(BSID)
        BSNodeName = IDToBSName(ID)
        BSIndex = BSIDToIndex(BSID)
        if not cmds.objExists(BSNodeName):
            cmds.blendShape(BSTargetName, pageName, name=BSNodeName)
            skinCluster = IDToSkinClusterName(ID)
            meshShapeNode = IDToMeshShapeNode(ID)
            if cmds.objExists(skinCluster):
                try:
                    cmds.reorderDeformers(skinCluster, BSNodeName, meshShapeNode)
                except:
                    pass
        else:
            cmds.blendShape(BSNodeName, edit=True, target=(pageName, BSIndex, BSTargetName, 1.0))


def disableBS(ID):
    BSNodeName = IDToBSName(ID)
    plugHandle = '.envelope'
    cmds.setAttr(BSNodeName + plugHandle, 0)


def enableBS(ID):
    BSNodeName = IDToBSName(ID)
    plugHandle = '.envelope'
    cmds.setAttr(BSNodeName + plugHandle, 1)


def resetControler(ID, cvsMaxIndex, width):
    cvsPosList = getCVsPosList(cvsMaxIndex, width)
    for cvsIndex in range(len(cvsPosList)):
        controler = IDToControlerName(ID) + '_' + str(cvsIndex)
        cmds.setAttr(f'{controler}.tx', cvsPosList[cvsIndex][0])
        cmds.setAttr(f'{controler}.ty', cvsPosList[cvsIndex][1])


# 自动引导 test only
def autoGuides():
    cmds.setAttr('MB_Controller_LL_0.tx', 0)
    cmds.setAttr('MB_Controller_LL_0.ty', 0)
    cmds.setAttr('MB_Controller_LL_1.tx', -2)
    cmds.setAttr('MB_Controller_LL_1.ty', 1)
    cmds.setAttr('MB_Controller_LL_2.tx', -6)
    cmds.setAttr('MB_Controller_LL_2.ty', 1)
    cmds.setAttr('MB_Controller_LL_3.tx', -10)
    cmds.setAttr('MB_Controller_LL_3.ty', 0)

    cmds.setAttr('MB_Controller_LR_0.tx', 0)
    cmds.setAttr('MB_Controller_LR_0.ty', 0)
    cmds.setAttr('MB_Controller_LR_1.tx', -1)
    cmds.setAttr('MB_Controller_LR_1.ty', 2)
    cmds.setAttr('MB_Controller_LR_2.tx', -4)
    cmds.setAttr('MB_Controller_LR_2.ty', 3)
    cmds.setAttr('MB_Controller_LR_3.tx', -9)
    cmds.setAttr('MB_Controller_LR_3.ty', 1)

    cmds.setAttr('MB_Controller_RL_0.tx', 0)
    cmds.setAttr('MB_Controller_RL_0.ty', 0)
    cmds.setAttr('MB_Controller_RL_1.tx', 1)
    cmds.setAttr('MB_Controller_RL_1.ty', 2)
    cmds.setAttr('MB_Controller_RL_2.tx', 4)
    cmds.setAttr('MB_Controller_RL_2.ty', 3)
    cmds.setAttr('MB_Controller_RL_3.tx', 9)
    cmds.setAttr('MB_Controller_RL_3.ty', 1)

    cmds.setAttr('MB_Controller_RR_0.tx', 0)
    cmds.setAttr('MB_Controller_RR_0.ty', 0)
    cmds.setAttr('MB_Controller_RR_1.tx', 2)
    cmds.setAttr('MB_Controller_RR_1.ty', 1)
    cmds.setAttr('MB_Controller_RR_2.tx', 6)
    cmds.setAttr('MB_Controller_RR_2.ty', 1)
    cmds.setAttr('MB_Controller_RR_3.tx', 10)
    cmds.setAttr('MB_Controller_RR_3.ty', 0)


def autoMiddles():
    cmds.setAttr('MB_Controller_Mid0_0.tx', 0)
    cmds.setAttr('MB_Controller_Mid0_0.ty', 0)
    cmds.setAttr('MB_Controller_Mid0_1.tx', -2)
    cmds.setAttr('MB_Controller_Mid0_1.ty', 3)
    cmds.setAttr('MB_Controller_Mid0_2.tx', -5)
    cmds.setAttr('MB_Controller_Mid0_2.ty', 5)
    cmds.setAttr('MB_Controller_Mid0_3.tx', -6)
    cmds.setAttr('MB_Controller_Mid0_3.ty', 8)

    cmds.setAttr('MB_Controller_Mid2_0.tx', 0)
    cmds.setAttr('MB_Controller_Mid2_0.ty', 0)
    cmds.setAttr('MB_Controller_Mid2_1.tx', 2)
    cmds.setAttr('MB_Controller_Mid2_1.ty', 3)
    cmds.setAttr('MB_Controller_Mid2_2.tx', 5)
    cmds.setAttr('MB_Controller_Mid2_2.ty', 5)
    cmds.setAttr('MB_Controller_Mid2_3.tx', 6)
    cmds.setAttr('MB_Controller_Mid2_3.ty', 8)


def createCmptCore(index, totalIndex, totalMiddles, cvsMaxIndex):
    ID = indexToID(index)
    guideIDs = ['LL', 'LR', 'RL', 'RR']
    cmptCoreName = IDToCmptCore(ID)
    MBCmptCore = cmds.createNode('MBCmptCore', name=cmptCoreName)
    cmds.setAttr(f'{MBCmptCore}.cvs', cvsMaxIndex)
    cmds.setAttr(f'{MBCmptCore}.index', index)
    cmds.setAttr(f'{MBCmptCore}.totalMiddles', totalMiddles)
    cmds.setAttr(f'{MBCmptCore}.totalIndex', totalIndex)

    for i, guideID in enumerate(guideIDs):
        guideController = IDToControlerName(guideID)
        for j in range(cvsMaxIndex):
            t = cvsMaxIndex * i + j
            cmds.connectAttr(f'{guideController}_{j}.translate', f'{cmptCoreName}.iGuidePCG[{t}]')

    MiddleIDs = indexToMiddleIDs(totalMiddles)
    for i, middleID in enumerate(MiddleIDs):
        middleController = IDToControlerName(middleID)
        for j in range(cvsMaxIndex):
            t = cvsMaxIndex * i + j
            cmds.connectAttr(f'{middleController}_{j}.translate', f'{cmptCoreName}.iMiddlePCG[{t}]')

    pageController = IDToControlerName(ID)
    for i in range(cvsMaxIndex):
        pageControllersuffix = addSuffix(pageController, i)
        cmds.connectAttr(f'{cmptCoreName}.oPCG[{i}]', f'{pageControllersuffix}.translate')


def createBookSpineCurve():
    bookSpineCurve = 'MB_BookSpine_Curve'
    deleteIfExist(bookSpineCurve)
    bookSpineCurve = cmds.curve(name=bookSpineCurve, p=[[-1, 0, 0], [0, 0, 0], [0, 0, 0], [1, 0, 0]])
    cmds.parent(bookSpineCurve, 'BookSpine')
    children = cmds.listRelatives(bookSpineCurve, children=True, fullPath=False)
    bookSpineCurveShapeName = 'MB_BookSpine_Curve_Shape'
    cmds.rename(children[0], bookSpineCurveShapeName)
    cmds.setAttr(f'{bookSpineCurve}.overrideEnabled', True)
    cmds.setAttr(f'{bookSpineCurve}.overrideColor', 17)
    cvsGrp = cmds.createNode('transform', n='MB_BookSpine_CVs')
    cmds.parent(cvsGrp, 'BookSpine')

    for i in range(4):
        jointName = f'MB_BookSpline_CV_{i}'
        deleteIfExist(jointName)
        joint = cmds.createNode('joint', name=jointName)
        cmds.setAttr(f'{joint}.tz', lock=True)
        cmds.setAttr(f'{joint}.rx', keyable=False)
        cmds.setAttr(f'{joint}.rz', keyable=False)
        cmds.setAttr(f'{joint}.ry', keyable=False)
        cmds.setAttr(f'{joint}.sx', keyable=False)
        cmds.setAttr(f'{joint}.sz', keyable=False)
        cmds.setAttr(f'{joint}.sy', keyable=False)
        cmds.parent(joint, cvsGrp)
        cmds.connectAttr(f'{joint}.translate', f'{bookSpineCurveShapeName}.controlPoints[{i}]')

    cmds.setAttr('MB_BookSpline_CV_0.v', False)
    cmds.setAttr('MB_BookSpline_CV_1.v', False)
    cmds.setAttr('MB_BookSpline_CV_1.radius', 0.5)
    cmds.setAttr('MB_BookSpline_CV_2.radius', 0.5)
    mult = cmds.createNode('multDoubleLinear')
    cmds.setAttr(f'{mult}.input2', -1)
    cmds.connectAttr('MB_BookSpline_CV_3.tx', f'{mult}.input1')
    cmds.connectAttr(f'{mult}.output', 'MB_BookSpline_CV_0.tx')

    mult = cmds.createNode('multDoubleLinear')
    cmds.setAttr(f'{mult}.input2', -1)
    cmds.connectAttr('MB_BookSpline_CV_2.tx', f'{mult}.input1')
    cmds.connectAttr(f'{mult}.output', 'MB_BookSpline_CV_1.tx')

    cmds.connectAttr('MB_BookSpline_CV_2.ty', 'MB_BookSpline_CV_1.ty')
    cmds.connectAttr('MB_BookSpline_CV_3.ty', 'MB_BookSpline_CV_0.ty')

    cmds.setAttr(f'{cvsGrp}.tz', 8)
    cmds.setAttr(f'{bookSpineCurve}.tz', 8)


def createPointOnCurveNode(ID):
    spineCurve = 'MB_BookSpine_Curve'
    controlCrv = IDToCrvName(ID)
    pointOnCurveName = IDToPointOnCurve(ID)
    deleteIfExist(pointOnCurveName)
    pointOnCurve = cmds.createNode('pointOnCurveInfo', n=pointOnCurveName)
    cmds.connectAttr(f'{spineCurve}.local', f'{pointOnCurve}.inputCurve')
    cmds.connectAttr(f'{pointOnCurve}.result.position', f'{controlCrv}.translate')
    cmptCore = IDToCmptCore(ID)
    if cmds.objExists(cmptCore):
        cmds.connectAttr(f'{cmptCore}.pp', f'{pointOnCurve}.parameter')
    elif ID == 'LL' or ID == 'RL':
        cmds.setAttr(f'{pointOnCurve}.parameter', 0)
    else:
        cmds.setAttr(f'{pointOnCurve}.parameter', 1)


def createRemap(totalIndex, ID, totalLocator):
    # create fence
    fence = f'MB_{ID}_Fence'
    deleteIfExist(fence)
    cmds.curve(name=fence, d=1, p=[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0)])
    cmds.setAttr(f'{fence}.overrideEnabled', True)
    cmds.setAttr(f'{fence}.overrideColor', 17)
    cmds.parent(fence, 'RemapController')
    # create display curve
    crv = f'MB_{ID}_Crv'
    cmds.curve(name=crv, d=1, p=[(i, 0, 0) for i in range(totalLocator)])
    cmds.parent(crv, fence)
    cmds.setAttr(f'{crv}.overrideEnabled', True)
    cmds.setAttr(f'{crv}.overrideColor', 18)

    # create remap node 'MB_Remap_' + ID
    remapNodeName = IDToRemapID(ID)
    remapNode = cmds.createNode('MBRemap', n=remapNodeName)
    cmds.setAttr(f'{remapNode}.totalIndex', totalIndex)
    cmds.setAttr(f'{remapNode}.totalLocator', totalLocator)
    for iindex in range(totalLocator):
        # iID = indexToID(iindex)
        remapControllerLoc = ID + str(iindex)
        foreRemapControllerLoc = ID + str(iindex - 1)
        cmds.createNode('joint', n=remapControllerLoc)
        cmds.parent(remapControllerLoc, 'RemapController')
        xValue = iindex / totalLocator / 2 + 0.5
        cmds.setAttr(f'{remapControllerLoc}.tx', iindex / (totalLocator - 1))
        cmds.setAttr(f'{remapControllerLoc}.ty', 0.5)
        cmds.connectAttr(f'{remapControllerLoc}.translate', f'{remapNode}.locator[{iindex}]')
        cmds.parent(remapControllerLoc, fence)
        cmds.setAttr(f'{remapControllerLoc}.tz', lock=True)
        cmds.setAttr(f'{remapControllerLoc}.rx', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.ry', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.rz', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.sx', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.sy', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.sz', keyable=False)
        cmds.setAttr(f'{remapControllerLoc}.minTransXLimitEnable', True)
        cmds.setAttr(f'{remapControllerLoc}.maxTransXLimitEnable', True)
        cmds.setAttr(f'{remapControllerLoc}.minTransYLimitEnable', True)
        cmds.setAttr(f'{remapControllerLoc}.maxTransYLimitEnable', True)
        if iindex == 0:
            cmds.setAttr(f'{remapControllerLoc}.minTransXLimit', 0)
        else:

            cmds.connectAttr(f'{foreRemapControllerLoc}.tx', f'{remapControllerLoc}.minTransXLimit')

        cmds.setAttr(f'{remapControllerLoc}.minTransYLimit', 0)
        cmds.connectAttr(f'{remapControllerLoc}.translate', f'{crv}.controlPoints[{iindex}]')
    cmds.setAttr(f'{fence}.sx', 6)
    cmds.setAttr(f'{fence}.sy', 6)
    cmds.setAttr(f'{fence}.sz', 6)

    if ID == 'cmpt':
        cmds.setAttr(f'{fence}.tx', 12)
    else:
        index = BSIDToIndex(ID)
        cmds.setAttr(f'{fence}.tx', -18)
        cmds.setAttr(f'{fence}.ty', 7 * index)


def conductRemap(ID, totalIndex, target):
    fence = f'MB_{ID}_Fence'
    # remapNodeName:'MB_Remap_' + ID
    remapNodeName = IDToRemapID(ID)
    for index in range(-totalIndex, totalIndex + 1):
        ID = indexToID(index)
        cmptCore = IDToCmptCore(ID)
        iindex = index + totalIndex
        if target == 'cmptCore':
            cmds.connectAttr(f'{remapNodeName}.remapValue[{iindex}]', f'{cmptCore}.ratio')
        else:
            BSName = indexToBSName(index)
            BSMeshID = IDToMeshShapeNode(target)
            cmds.connectAttr(f'{remapNodeName}.remapValue[{iindex}]', f'{BSName}.{BSMeshID}')
            cmds.setAttr(f'{fence}.overrideEnabled', True)
            cmds.setAttr(f'{fence}.overrideColor', 23)


def createCloseAttr(width, cvsMaxIndex, guideIDs, totalMiddles):
    cmds.addAttr('Main', ln='close', attributeType="float", defaultValue=1.0, minValue=0.0, maxValue=1.0)
    MiddleIDs = indexToMiddleIDs(totalMiddles)
    IDs = guideIDs[:2]
    IDs.append(MiddleIDs)
    IDs.append(guideIDs[2:])
    for index in range(totalMiddles + 4):
        ID = indexToID(index)
        controller = IDToControlerName(ID)
        for cv in range(cvsMaxIndex):
            nodeName = addSuffix(controller, cv)
            connections = cmds.listConnections(f'{nodeName}.translate', source=True, destination=False, plugs=True)
            multiply_node = cmds.createNode('multiplyDivide')
            add_node = cmds.createNode('addDoubleLinear')
            # 设置乘数节点的输入1为原始的translate属性
            cmds.connectAttr(f'{nodeName}.translate', multiply_node + '.input1')
            cmds.connectAttr('Main.close', multiply_node + '.input2')

            # 将乘数节点的输出连接到其他节点
            for destination_plug in connections:
                cmds.connectAttr(f'{multiply_node}.output', destination_plug, force=True)


def find_files_in_folder(directory, prefix='', suffix=''):
    all_files = os.listdir(directory)
    filtered_files = [file for file in all_files if file.startswith(prefix) and file.endswith(suffix)]
    file_paths = [os.path.join(directory, file) for file in filtered_files]

    return file_paths


def doubleSideShader(shaderName, BSDF, textureFilePath1, textureFilePath2, roughness):
    textureName1 = shaderName + '_T1'
    textureName2 = shaderName + '_T2'
    conditionName = shaderName + '_Con'
    samplerInfoName = shaderName + '_Sam'

    deleteIfExist(shaderName)
    deleteIfExist(textureName1)
    deleteIfExist(textureName2)
    deleteIfExist(conditionName)
    deleteIfExist(samplerInfoName)
    # create nodes
    shader = cmds.shadingNode(BSDF, name=shaderName, asShader=True)
    texture1 = cmds.shadingNode('file', name=textureName1, asTexture=True)
    texture2 = cmds.shadingNode('file', name=textureName2, asTexture=True)
    condition = cmds.shadingNode('condition', asUtility=True, name=conditionName)
    samplerInfo = cmds.shadingNode('samplerInfo', asUtility=True, name=samplerInfoName)

    # connect and set attribute
    cmds.connectAttr(f'{texture1}.outColor', f'{condition}.colorIfTrue')
    cmds.connectAttr(f'{texture2}.outColor', f'{condition}.colorIfFalse')
    cmds.connectAttr(f'{samplerInfo}.flippedNormal', f'{condition}.firstTerm')
    cmds.connectAttr(f'{condition}.outColor', f'{shader}.baseColor')
    cmds.setAttr(f'{texture1}.fileTextureName', textureFilePath1, type='string')
    cmds.setAttr(f'{texture2}.fileTextureName', textureFilePath2, type='string')
    cmds.setAttr(f'{shader}.specularRoughness', roughness)


def assignPageShader(totalIndex, path, BSDF, roughness, prefix='', suffix=''):
    for index in range(-totalIndex, totalIndex + 1):
        ID = indexToID(index)
        meshName = indexToMeshName(index)
        shaderID = IDToShaderID(ID)
        lIndex = index + totalIndex
        file_paths = find_files_in_folder(path, prefix, suffix)
        fileCount = len(file_paths)
        if fileCount % 2:
            return
        if lIndex < fileCount / 2:
            filePath1 = file_paths[lIndex * 2]
            filePath2 = file_paths[lIndex * 2 + 1]
            doubleSideShader(shaderID, BSDF, filePath1, filePath2, roughness)
            cmds.select(meshName)
            cmds.hyperShade(shaderID, assign=shaderID)
        else:
            shaderID = IDToShaderID(indexToID(int(fileCount / 2 - totalIndex - 1)))
            cmds.select(meshName)
            cmds.hyperShade(shaderID, assign=shaderID)


def MBRig(totalIndex,width,height,subDivWidth,subDivHeight,cvsMaxIndex,totalMiddles,totalBSs,totalFlipRemapLocator,totalBSRemapLocator):
    shaderColorList = [(29, 43, 83), (126, 37, 83), (255, 0, 77), (250, 239, 93),  # cv controllers
                       (54, 84, 134), (255, 0, 77), (250, 239, 93),  # LGuides, RGuides, Middles
                       (67, 118, 108),  # BSMesh
                       (126, 37, 83)]
    guideIDs = ['LL', 'LR', 'RL', 'RR']
    BSIDs = totalBSsToBSIDs(totalBSs)
    remapID = 'cmpt'
    createMBShader(shaderColorList)
    createRigTree()

    # 创建引导
    createGuides(width, height, subDivWidth, subDivHeight, cvsMaxIndex)
    # 创建中间页
    createMiddles(totalMiddles, width, height, subDivWidth, subDivHeight, cvsMaxIndex)
    # 循环 创建MBPage
    for iindex in range(-totalIndex, totalIndex + 1):
        ID = indexToID(iindex)
        createPage(ID, width, height, subDivWidth, subDivHeight, cvsMaxIndex)

    # 创建BS
    createBSTarget(BSIDs, width, height, subDivWidth, subDivHeight)
    # 循环 应用BS
    for iindex in range(-totalIndex, totalIndex + 1):
        ID = indexToID(iindex)
        conductBS(BSIDs, ID)

    # 循环 创建MB计算核心
    for iindex in range(-totalIndex, totalIndex + 1):
        ID = indexToID(iindex)
        createCmptCore(iindex, totalIndex, totalMiddles, cvsMaxIndex)

    # 创建书脊
    createBookSpineCurve()

    # 循环 创建点在线上，偏移书页
    for iindex in range(-totalIndex, totalIndex + 1):
        ID = indexToID(iindex)
        createPointOnCurveNode(ID)

    # 循环 偏移guide
    for ID in guideIDs:
        createPointOnCurveNode(ID)

    # 创建Remap节点并应用
    createRemap(totalIndex, 'cmpt', totalFlipRemapLocator)
    conductRemap('cmpt', totalIndex, 'cmptCore')

    # 创建BS的Remap节点并应用
    for BSID in BSIDs:
        createRemap(totalIndex, BSID, totalBSRemapLocator)
        conductRemap(BSID, totalIndex, BSID)

# 定义参数
totalIndex = 10
width = 10
height = 15
subDivWidth = 7
subDivHeight = 10
cvsMaxIndex = 4  # 修改这个会让自动放置失效
totalMiddles = 3  # 修改这个会让自动放置失效
totalBSs = 2
totalFlipRemapLocator = 4
totalBSRemapLocator = 3

# 创建Rig
cmds.file(new=True, force=True)
MBRig(totalIndex,width,height,subDivWidth,subDivHeight,cvsMaxIndex,totalMiddles,totalBSs,totalFlipRemapLocator,totalBSRemapLocator)
autoGuides()
autoMiddles()

# 分发材质
path = r'E:\P\Magician\maya\sourceimages\MBTexture'
prefix = ''
suffix = '.jpg'
BSDF = 'aiStandardSurface'
roughness = 0.7
assignPageShader(totalIndex, path, BSDF, roughness, prefix='', suffix='.jpg')