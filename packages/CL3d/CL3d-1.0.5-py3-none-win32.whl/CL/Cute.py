from CL.Display.SimpleGui import init_display
from CL.process import initGui
from CL.lib.Base import Display as Dis
from CL.lib.Menu import initMenu
from CL.res.dark_blue_qss import qss
import pickle
from CL.lib.Base import Data


def init(par_win=None):
    display, start_display, get_Viewer3d, add_function_to_menu = init_display(par_win=par_win)
    initMenu(get_Viewer3d, add_function_to_menu)
    Dis.display = display
    Dis.CDisplay = display.Context.Display
    Dis.CUpdate = display.Context.UpdateCurrentViewer
    Dis.C = display.Context
    Dis.Win = get_Viewer3d()
    Dis.Drawer = display.Context.DefaultDrawer()
    # 获取occ窗口
    Viewer3d_Win = get_Viewer3d()
    # 设置全局样式表
    init = initGui.InitGui(Viewer3d_Win)
    # 读文件
    # styleFile = 'res/dark-blue.qss'
    # qssStyle = init.readQss(styleFile)
    # Viewer3d_Win.setStyleSheet(qssStyle)
    # 读变量
    Viewer3d_Win.setStyleSheet(qss)
    # 添加界面
    Dis.mainWin = init.initMainGui()    # 这个是Action实例

    def start():
        start_display()
        # 保存上次打开的目录
        if Data.lastOpendPath:
            with open('lastdir.conf', 'wb') as f:
                pickle.dump(Data.lastOpendPath, f)

    Viewer3d_Win.start = start
    return Viewer3d_Win



