# import maya.cmds as cmds
# cmds.file(new=True, force=True)
# cubic = cmds.createNode('MBCubic')
# cubic2 = cmds.createNode('MBCubic')
# trans = cmds.createNode('transform')
# cmds.setAttr(f'{trans}.tx', 0.0)
# cmds.setAttr(f'{trans}.ty', 0.5)
# cmds.setAttr(f'{trans}.tz', 1)
# cmds.connectAttr(f'{trans}.tx', f'{cubic}.index[0]')
# cmds.connectAttr(f'{trans}.ty', f'{cubic}.index[1]')
# cmds.connectAttr(f'{trans}.tz', f'{cubic}.index[2]')
#
# cmds.connectAttr(f'{cubic}.prj[0]', f'{cubic2}.index[0]')
# cmds.connectAttr(f'{cubic}.prj[1]', f'{cubic2}.index[1]')
# cmds.connectAttr(f'{cubic}.prj[2]', f'{cubic2}.index[2]')

import maya.cmds as cmds
cmds.file(new=True, force=True)
totalIndex = 10
remap = cmds.createNode('MBRemap')
totalCtrlor=4
for i in range(totalCtrlor):
    transform = cmds.createNode('transform')

    cmds.setAttr(f'{transform}.tx',i/ (totalCtrlor-1))
    cmds.setAttr(f'{transform}.ty', i / (totalCtrlor-1))
    cmds.connectAttr(f'{transform}.translate',f'{remap}.locator[{i}]')


for i in range(-totalIndex,totalIndex+1):
    listi = totalIndex+i
    joint = cmds.createNode('joint')
    xvalue = (i / totalIndex) / 2 + 0.5
    cmds.setAttr(f'{joint}.tx',xvalue)
    cmds.setAttr(f'{joint}.radius',0.5)
    cmds.connectAttr(f'{remap}.remapValue[{listi}]',f'{joint}.ty')

cmds.select(remap)