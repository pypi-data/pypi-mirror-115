from CL.Display.OCCViewer import rgb_color

from CL.lib import Action
from CL.process import MakeShape
from CL.process import RapidFeedUpdate
from OCC.Core.Prs3d import Prs3d_TypeOfHighlight_Dynamic, Prs3d_TypeOfHighlight_Selected,\
Prs3d_TypeOfHighlight_LocalSelected, Prs3d_TypeOfHighlight_LocalDynamic

class InitGui(object):
    def __init__(self, win):
        self.mainWin = Action.Action(win)
        # 设置高亮选中状态颜色和模式 （LocalSelected 设置非SelectionMode(0)下的样式）
        # 设置的对象为from OCC.Core.PrsMgr import PrsMgr_PresentableObject
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_Selected).SetColor(rgb_color(0, 1, 0))
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_Selected).SetDisplayMode(1)
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_LocalSelected).SetColor(rgb_color(0, 1, 0))
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_LocalSelected).SetDisplayMode(1)
        # self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_Dynamic).SetColor(rgb_color(1, 1, 0))
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_Dynamic).SetDisplayMode(1)
        self.mainWin.Context.HighlightStyle(Prs3d_TypeOfHighlight_LocalDynamic).SetDisplayMode(1)

        # 设置偏离角， 提高曲线显示质量SetDeviationCoefficient 精确绘制
        self.mainWin.Context.SetDeviationCoefficient(0.001)
        self.mainWin.Context.SetDeviationAngle(0.05)  # default 0.209440
        # self.mainWin.Context.SetHLRDeviationCoefficient(0.02)
        # self.mainWin.Context.SetHLRAngle(0.05)  # default 0.349066

        # 设置选择像素公差
        self.mainWin.Context.MainSelector().SetPixelTolerance(10)

    def initMainGui(self):
        return self.mainWin

    def readQss(self, style):
        with open(style, 'r') as f:
            return f.read()
