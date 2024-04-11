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
    totalIndex = cmds.intFieldGrp(label="Number of Page Per Side = ", value1=10, adjustableColumn2=1)
    width = cmds.floatFieldGrp(label="Width = ", value1=10.0, adjustableColumn2=1)
    height = cmds.floatFieldGrp(label="Height = ", value1=15.0, adjustableColumn2=1)
    subDivWidth = cmds.intFieldGrp(label="SubDivWidth = ", value1=7, adjustableColumn2=1)
    subDivHeight = cmds.intFieldGrp(label="SubDivHeight = ", value1=10, adjustableColumn2=1)
    cvsMaxIndex = cmds.intFieldGrp(label="* Number of CV Points on Curve = ", value1=4, adjustableColumn2=1)
    totalMiddles = cmds.intFieldGrp(label="* Number of Middle Page Count = ", value1=3, adjustableColumn2=1)
    totalBSs = cmds.intFieldGrp(label="Number of BlendShape Target = ", value1=2, adjustableColumn2=1)
    totalFlipRemapLocator = cmds.intFieldGrp(label="Number of Ctrl Points for Flip = ", value1=6, adjustableColumn2=1)
    totalBSRemapLocator = cmds.intFieldGrp(label="Number of Ctrl Points for BS = ", value1=5, adjustableColumn2=1)

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
    cmds.text('Auto Funcs Only Work When Param with * Has Default Value',height = 20)
    cmds.button(label='AutoGuides', command=lambda *args: MBFuncs.autoGuides())
    cmds.button(label='AutoMiddles', command=lambda *args: MBFuncs.autoMiddles())
    # cmds.button(label='reset selected controllers',
    #             command=lambda *args: MBFuncs.resetSelectedControler(
    #                 cmds.intFieldGrp(cvsMaxIndex, query=True, value1=True),
    #                 cmds.floatFieldGrp(width, query=True, value1=True)
    #                 )
    #             )
    cmds.setParent('..')

    # 创建第二个标签页
    child2 = cmds.columnLayout("PageShaderLayout", adjustableColumn=True, columnAlign="center")

    # 创建输入字段
    # pageTotalIndex = cmds.intFieldGrp(label="totalIndex = ", value1=10, adjustableColumn2=2)
    path = cmds.textFieldGrp(label="path = ", text=r'', adjustableColumn2=2)
    BSDF = cmds.textFieldGrp(label="BSDF = ", text='aiStandardSurface', adjustableColumn2=2)
    cprefix = cmds.textFieldGrp(label="color prefix = ", text='c_', adjustableColumn2=2)
    csuffix = cmds.textFieldGrp(label="color suffix = ", text='', adjustableColumn2=2)
    rprefix = cmds.textFieldGrp(label="roughness prefix = ", text='r_', adjustableColumn2=2)
    rsuffix = cmds.textFieldGrp(label="roughness suffix = ", text='', adjustableColumn2=2)
    mprefix = cmds.textFieldGrp(label="metalness prefix = ", text='m_', adjustableColumn2=2)
    msuffix = cmds.textFieldGrp(label="metalness suffix = ", text='', adjustableColumn2=2)
    cmds.text(label='! extension is also considered in suffix !',height = 20)
    # 创建按钮
    cmds.button(label="Execute",
                command=lambda *args: MBFuncs.assignPageShader(
                    #cmds.intFieldGrp(pageTotalIndex, query=True, value1=True),
                    cmds.textFieldGrp(path, query=True, text=True),
                    cmds.textFieldGrp(BSDF, query=True, text=True),
                    cmds.textFieldGrp(cprefix, query=True, text=True),
                    cmds.textFieldGrp(csuffix, query=True, text=True),
                    cmds.textFieldGrp(rprefix, query=True, text=True),
                    cmds.textFieldGrp(rsuffix, query=True, text=True),
                    cmds.textFieldGrp(mprefix, query=True, text=True),
                    cmds.textFieldGrp(msuffix, query=True, text=True)
                ))

    cmds.setParent('..')

    # 添加标签页
    cmds.tabLayout(tabs, edit=True, tabLabel=((child1, 'MBRig'), (child2, 'PageShader')))

    # 显示窗口
    cmds.showWindow(myWindow)
