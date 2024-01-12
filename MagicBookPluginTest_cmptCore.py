import maya.cmds as cmds
cmds.file(new=True,force=True)

cmptCore = cmds.createNode('MBCmptCore')
transform0 = cmds.createNode('transform')
transform1 = cmds.createNode('transform')
transform2 = cmds.createNode('transform')
transform3 = cmds.createNode('transform')
# cmds.connectAttr(f'{transform}.translate',f'{cmptCore}.iPCGsList[0].iPCG[0]')
# cmds.getAttr(f'{cmptCore}.index')

for i in range(20):
    transform = cmds.createNode('transform')
    tValue = i
    cmds.setAttr(f'{transform}.tx',tValue)
    cmds.connectAttr(f'{transform}.translate',f'{cmptCore}.iGuidePCG[{i}]')

for i in range(15):
    transform = cmds.createNode('transform')
    tValue = i
    cmds.setAttr(f'{transform}.tx', tValue)
    cmds.connectAttr(f'{transform}.translate', f'{cmptCore}.iMiddlePCG[{i}]')

CVs = 5
for i in range(CVs):
    joint = cmds.createNode('joint')
    cmds.connectAttr(f'{cmptCore}.oPCG[{i}]',f'{joint}.translate')