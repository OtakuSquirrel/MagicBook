import maya.cmds as cmds
import importlib
def UI():

    import MBFuncs
    importlib.reload(MBFuncs)

    plugin_name = 'MagicBookPlugin.py'
    if not cmds.pluginInfo(plugin_name, q=True, loaded=True): cmds.loadPlugin(plugin_name)

    # 创建窗口
    # if cmds.window("mywindow1", exists=True):
    #     cmds.deleteUI("mywindow1", window=True)
    # myWindow = cmds.window("mywindow1", title="MagicBook", widthHeight=(400, 300))
    myWindow = cmds.window(title="MagicBook", widthHeight=(400, 340))
    # 创建tab布局
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

    # 创建第一个标签页
    child1 = cmds.columnLayout("MBRigLayout", adjustableColumn=True, columnAlign="center")

    # 创建输入字段
    totalIndex = cmds.intFieldGrp(label="totalIndex = ", value1=10, adjustableColumn2=2)
    width = cmds.floatFieldGrp(label="width = ", value1=10.0, adjustableColumn2=2)
    height = cmds.floatFieldGrp(label="height = ", value1=15.0, adjustableColumn2=2)
    subDivWidth = cmds.intFieldGrp(label="subDivWidth = ", value1=7, adjustableColumn2=2)
    subDivHeight = cmds.intFieldGrp(label="subDivHeight = ", value1=10, adjustableColumn2=2)
    cvsMaxIndex = cmds.intFieldGrp(label="cvsMaxIndex = ", value1=4, adjustableColumn2=2)
    totalMiddles = cmds.intFieldGrp(label="totalMiddles = ", value1=3, adjustableColumn2=2)
    totalBSs = cmds.intFieldGrp(label="totalBSs = ", value1=2, adjustableColumn2=2)
    totalFlipRemapLocator = cmds.intFieldGrp(label="totalFlipRemapLocator = ", value1=4, adjustableColumn2=2)
    totalBSRemapLocator = cmds.intFieldGrp(label="totalBSRemapLocator = ", value1=5, adjustableColumn2=2)

    # 创建按钮
    cmds.button(label="Execute",
                command=lambda *args: MBFuncs.MBRig(
                    cmds.intFieldGrp(totalIndex, query=True, value1=True),
                    cmds.floatFieldGrp(width, query=True, value1=True),
                    cmds.floatFieldGrp(height, query=True, value1=True),
                    cmds.intFieldGrp(subDivWidth, query=True, value1=True),
                    cmds.intFieldGrp(subDivHeight, query=True, value1=True),
                    cmds.intFieldGrp(cvsMaxIndex, query=True, value1=True),
                    cmds.intFieldGrp(totalMiddles, query=True, value1=True),
                    cmds.intFieldGrp(totalBSs, query=True, value1=True),
                    cmds.intFieldGrp(totalFlipRemapLocator, query=True, value1=True),
                    cmds.intFieldGrp(totalBSRemapLocator, query=True, value1=True)
                )
                )

    cmds.button(label='AutoGuides(Only work with default value)',command=lambda *args: MBFuncs.autoGuides())
    cmds.button(label='AutoMiddles(Only work with default value)', command=lambda *args: MBFuncs.autoMiddles())

    cmds.setParent('..')

    # 创建第二个标签页
    child2 = cmds.columnLayout("PageShaderLayout", adjustableColumn=True, columnAlign="center")

    # 创建输入字段
    path = cmds.textFieldGrp(label="path = ", text=r'', adjustableColumn2=2)
    prefix = cmds.textFieldGrp(label="prefix = ", text='', adjustableColumn2=2)
    suffix = cmds.textFieldGrp(label="suffix = ", text='.jpg', adjustableColumn2=2)
    BSDF = cmds.textFieldGrp(label="BSDF = ", text='aiStandardSurface', adjustableColumn2=2)
    roughness = cmds.textFieldGrp(label="roughness = ", adjustableColumn2=2)

    # 创建按钮
    cmds.button(label="Execute",
                command=lambda *args: MBFuncs.assignPageShader(
                    cmds.intFieldGrp(totalIndex, query=True, value1=True),
                    cmds.textFieldGrp(path, query=True, text=True),
                    cmds.textFieldGrp(BSDF, query=True, text=True),
                    cmds.textFieldGrp(roughness, query=True, text=True),
                    cmds.textFieldGrp(prefix, query=True, text=True),
                    cmds.textFieldGrp(suffix, query=True, text=True)
                ))

    cmds.setParent('..')



    # 添加标签页
    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'MBRig'), (child2, 'PageShader')))

    # 显示窗口
    cmds.showWindow(myWindow)
