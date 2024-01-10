import maya.cmds as cmds


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


def indexToMeshName(index):
    meshName = 'MB_Mesh_' + indexToID(index)
    return meshName


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
    return 'MB_Ctrlor_' + ID


def controlerNameToID(controlerName):
    return controlerName[10:]


def IDToBSName(ID):
    return 'MB_BS_' + ID


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

def IDToFlipCtrlorLoc(ID):
    return f'MB_FCLoc_{ID}'
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

    levelName = 'GuideCurveGrp'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'BookSpine'
    parentName = 'Main'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)

    levelName = 'FlipCtrlor'
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

    levelName = 'BSGrp'
    parentName = 'DeformationSystem'
    deleteIfExist(levelName)
    cmds.createNode('transform', n=levelName, p=parentName)
    cmds.setAttr('BSGrp.v', False)


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
    if not (cmds.objExists(meshName) and cmds.objExists(jntName)):
        print(meshName, 'or', jntName, 'missing')
        return
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


def createControler(ID, width, cvsMaxIndex=4):
    controlerName = IDToControlerName(ID)
    curveName = IDToCrvName(ID)
    curveShapeName = IDToCrvShapeName(ID)
    cvsList = getCVsPosList(cvsMaxIndex, width)
    for i in range(cvsMaxIndex):
        controlerName_suffix = controlerName + '_' + str(i)
        cmds.sphere(name=controlerName_suffix, radius=0.5, sections=1)
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

        shaderName = f'MB_S_Ramp_{i}'
        cmds.hyperShade(assign=shaderName)


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
        createControler(ID, width, cvsMaxIndex)


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
        createControler(ID, width, cvsMaxIndex)


def createPage(ID, width, height, subDivWidth, subDivHeight, cvsMaxIndex):
    createMesh(ID, width, height, subDivWidth, subDivHeight)
    createJointChain(ID, width, subDivWidth)
    bindSkin(ID)
    injectJntWeight(ID, subDivWidth, subDivHeight)
    createCVCurve(ID, width, cvsMaxIndex)
    createIKHandle(ID, subDivWidth)
    createControler(ID, width, cvsMaxIndex)


def createBSTarget(BSIDs, width, height, subDivWidth, subDivHeight):
    shaderName = iToShaderName(7)
    for BSID in BSIDs:
        createMesh(BSID, width, height, subDivWidth, subDivHeight)
        cmds.hyperShade(assign=shaderName)
        BSName = IDToMeshName(BSID)
        cmds.parent(BSName, 'BSGrp')


def conductBS(BSIDs, ID):
    for BSID in BSIDs:
        pageName = IDToMeshName(ID)
        BSTargetName = IDToMeshName(BSID)
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
    cmds.setAttr('MB_Ctrlor_LL_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_LL_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_LL_1.tx', -2)
    cmds.setAttr('MB_Ctrlor_LL_1.ty', 1)
    cmds.setAttr('MB_Ctrlor_LL_2.tx', -6)
    cmds.setAttr('MB_Ctrlor_LL_2.ty', 1)
    cmds.setAttr('MB_Ctrlor_LL_3.tx', -10)
    cmds.setAttr('MB_Ctrlor_LL_3.ty', 0)

    cmds.setAttr('MB_Ctrlor_LR_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_LR_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_LR_1.tx', -1)
    cmds.setAttr('MB_Ctrlor_LR_1.ty', 2)
    cmds.setAttr('MB_Ctrlor_LR_2.tx', -4)
    cmds.setAttr('MB_Ctrlor_LR_2.ty', 3)
    cmds.setAttr('MB_Ctrlor_LR_3.tx', -9)
    cmds.setAttr('MB_Ctrlor_LR_3.ty', 1)

    cmds.setAttr('MB_Ctrlor_RL_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_RL_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_RL_1.tx', 1)
    cmds.setAttr('MB_Ctrlor_RL_1.ty', 2)
    cmds.setAttr('MB_Ctrlor_RL_2.tx', 4)
    cmds.setAttr('MB_Ctrlor_RL_2.ty', 3)
    cmds.setAttr('MB_Ctrlor_RL_3.tx', 9)
    cmds.setAttr('MB_Ctrlor_RL_3.ty', 1)

    cmds.setAttr('MB_Ctrlor_RR_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_RR_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_RR_1.tx', 2)
    cmds.setAttr('MB_Ctrlor_RR_1.ty', 1)
    cmds.setAttr('MB_Ctrlor_RR_2.tx', 6)
    cmds.setAttr('MB_Ctrlor_RR_2.ty', 1)
    cmds.setAttr('MB_Ctrlor_RR_3.tx', 10)
    cmds.setAttr('MB_Ctrlor_RR_3.ty', 0)


def autoMiddles():
    cmds.setAttr('MB_Ctrlor_Mid0_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_Mid0_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_Mid0_1.tx', -2)
    cmds.setAttr('MB_Ctrlor_Mid0_1.ty', 3)
    cmds.setAttr('MB_Ctrlor_Mid0_2.tx', -5)
    cmds.setAttr('MB_Ctrlor_Mid0_2.ty', 5)
    cmds.setAttr('MB_Ctrlor_Mid0_3.tx', -6)
    cmds.setAttr('MB_Ctrlor_Mid0_3.ty', 8)

    cmds.setAttr('MB_Ctrlor_Mid2_0.tx', 0)
    cmds.setAttr('MB_Ctrlor_Mid2_0.ty', 0)
    cmds.setAttr('MB_Ctrlor_Mid2_1.tx', 2)
    cmds.setAttr('MB_Ctrlor_Mid2_1.ty', 3)
    cmds.setAttr('MB_Ctrlor_Mid2_2.tx', 5)
    cmds.setAttr('MB_Ctrlor_Mid2_2.ty', 5)
    cmds.setAttr('MB_Ctrlor_Mid2_3.tx', 6)
    cmds.setAttr('MB_Ctrlor_Mid2_3.ty', 8)


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
        guideCtrlor = IDToControlerName(guideID)
        for j in range(cvsMaxIndex):
            t = cvsMaxIndex * i + j
            cmds.connectAttr(f'{guideCtrlor}_{j}.translate', f'{cmptCoreName}.iGuidePCG[{t}]')

    MiddleIDs = indexToMiddleIDs(totalMiddles)
    for i, middleID in enumerate(MiddleIDs):
        middleCtrlor = IDToControlerName(middleID)
        for j in range(cvsMaxIndex):
            t = cvsMaxIndex * i + j
            cmds.connectAttr(f'{middleCtrlor}_{j}.translate', f'{cmptCoreName}.iMiddlePCG[{t}]')

    pageCtrlor = IDToControlerName(ID)
    for i in range(cvsMaxIndex):
        pageCtrlorsuffix = addSuffix(pageCtrlor, i)
        cmds.connectAttr(f'{cmptCoreName}.oPCG[{i}]', f'{pageCtrlorsuffix}.translate')


def createBookSpineCurve():
    bookSpineCurve = 'MB_BookSpine_Curve'
    deleteIfExist(bookSpineCurve)
    bookSpineCurve = cmds.curve(name=bookSpineCurve, p=[[-1, 0, 0], [0, 0, 0], [0, 0, 0], [1, 0, 0]])
    cmds.parent(bookSpineCurve, 'BookSpine')
    children = cmds.listRelatives(bookSpineCurve, children=True, fullPath=False)
    bookSpineCurveShapeName = 'MB_BookSpine_Curve_Shape'
    cmds.rename(children[0], bookSpineCurveShapeName)

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

    cmds.setAttr('MB_BookSpline_CV_0.v',False)
    cmds.setAttr('MB_BookSpline_CV_1.v', False)
    cmds.setAttr('MB_BookSpline_CV_2.v',False)
    mult = cmds.createNode('multDoubleLinear')
    cmds.setAttr(f'{mult}.input2',-1)
    cmds.connectAttr('MB_BookSpline_CV_3.tx',f'{mult}.input1')
    cmds.connectAttr(f'{mult}.output','MB_BookSpline_CV_0.tx')

    mult = cmds.createNode('multDoubleLinear')
    cmds.setAttr(f'{mult}.input2', -1)
    cmds.connectAttr('MB_BookSpline_CV_2.tx', f'{mult}.input1')
    cmds.connectAttr(f'{mult}.output', 'MB_BookSpline_CV_1.tx')

    cmds.connectAttr('MB_BookSpline_CV_2.ty', 'MB_BookSpline_CV_1.ty')

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
        cmds.setAttr(f'{pointOnCurve}.parameter',0)
    else:
        cmds.setAttr(f'{pointOnCurve}.parameter',1)


# 定义参数
totalIndex = 10
width = 10
height = 15
subDivWidth = 5
subDivHeight = 10
cvsMaxIndex = 4
totalMiddles = 3
totalBSs = 2
totalLocator = 6
shaderColorList = [(29, 43, 83), (126, 37, 83),
                   (255, 0, 77), (250, 239, 93),
                   (54, 84, 134), (255, 0, 77), (250, 239, 93),
                   (255, 0, 77), (126, 37, 83)]
guideIDs = ['LL', 'LR', 'RL', 'RR']
BSIDs = totalBSsToBSIDs(totalBSs)
# 准备
cmds.file(new=True, force=True)
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

# # 创建BS
# BSID = 'BS1'
# createBSTarget(BSID, width, height, subDivWidth, subDivHeight)
# # 循环 应用BS
# conductBS(BSID, ID)

# 自动中间页 test only
autoGuides()

autoMiddles()
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

def createRemap(totalIndex,totalLocator):
    remapNode = cmds.createNode('MBRemap')
    for index in range(totalLocator):
        ID = indexToID(index)
        flipCtrlorLoc = IDToFlipCtrlorLoc(ID)
        cmds.createNode('joint',n=flipCtrlorLoc)
        cmds.parent(flipCtrlorLoc,'FlipCtrlor')
        xValue = index/(totalLocator-1)
        cmds.setAttr(f'{flipCtrlorLoc}.tx',xValue)
        cmds.setAttr(f'{flipCtrlorLoc}.ty', 0.5)
        cmds.connectAttr(f'{flipCtrlorLoc}.translate',f'{remapNode}.locator[{index}]')

    # for index in range(totalIndex):
    #
    #     cmds.connectAttr()

createRemap(totalIndex,totalLocator)