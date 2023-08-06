

from __future__ import print_function

import logging
import os
import sys

from CL.Display import OCCViewer
from CL.Display.backend import get_qt_modules
from OCC.Core.AIS import AIS_Manipulator, AIS_Shape

from OCC.Core.gp import gp_Pnt
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from CL.Display.OCCViewer import rgb_color

QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

# check if signal available, not available
# on PySide
HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

# QtOpenGL.QGLWidget -> QtWidgets.QWidget
class qtBaseViewer(QtOpenGL.QGLWidget):
    ''' The base Qt Widget for an OCC viewer
    '''

    def __init__(self, parent=None):
        super(qtBaseViewer, self).__init__(parent)
        self._display = None
        self._inited = False

        # enable Mouse Tracking
        self.setMouseTracking(True)

        # Strong focus
        self.setFocusPolicy(QtCore.Qt.WheelFocus)

        # required for overpainting the widget
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)

        self.setAutoFillBackground(False)

    def GetHandle(self):
        ''' returns an the identifier of the GUI widget.
        It must be an integer
        '''
        win_id = self.winId()  # this returns either an int or voitptr
        if "%s" % type(win_id) == "<type 'PyCObject'>":  # PySide
            ### with PySide, self.winId() does not return an integer
            if sys.platform == "win32":
                ## Be careful, this hack is py27 specific
                ## does not work with python31 or higher
                ## since the PyCObject api was changed
                import ctypes
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
                win_id = ctypes.pythonapi.PyCObject_AsVoidPtr(win_id)
        elif not isinstance(win_id, int):  # PyQt4 or 5
            ## below integer cast may be required because self.winId() can
            ## returns a sip.voitptr according to the PyQt version used
            ## as well as the python version
            win_id = int(win_id)
        return win_id

    def resizeEvent(self, event):
        if self._inited:
            super(qtBaseViewer, self).resizeEvent(event)
            self._display.OnResize()


class qtViewer3d(qtBaseViewer):
    # emit signal when selection is changed
    # is a list of TopoDS_*
    if HAVE_PYQT_SIGNAL:
        sig_topods_selected = QtCore.pyqtSignal(list)

    def __init__(self, *kargs):
        qtBaseViewer.__init__(self, *kargs)

        self.setObjectName("qt_viewer_3d")

        self._drawbox = False
        self._zoom_area = False
        self._select_area = False
        self._inited = False
        self._leftisdown = False
        self._middleisdown = False
        self._rightisdown = False
        self._selection = None
        self._drawtext = True
        self._qApp = QtWidgets.QApplication.instance()
        self._key_map = {}
        self._current_cursor = "arrow"
        self._available_cursors = {}
        self.ais_manipulator = None
        self.ais_manipulator_shift = False
        self.ais_manipulator_starting = False
        self.dxdydzAdjust = None
        self.dynamic_mease = None

    @property
    def qApp(self):
        # reference to QApplication instance
        return self._qApp

    @qApp.setter
    def qApp(self, value):
        self._qApp = value

    def InitDriver(self):
        self._display = OCCViewer.Viewer3d(window_handle=self.GetHandle(), parent=self)
        self._display.Create()
        # background gradient
        self._display.SetModeShaded()
        self._inited = True
        # dict mapping keys to functions
        self._key_map = {
            # ord('W'): self._display.SetModeWireFrame,
            # ord('S'): self._display.SetModeShaded,
            # ord('A'): self._display.EnableAntiAliasing,
            # ord('B'): self._display.DisableAntiAliasing,
            # ord('H'): self._display.SetModeHLR,
            ord('F'): self._display.FitAll,
            ord('1'): lambda: self._display.tabWidget.setCurrentIndex(0),
            ord('2'): lambda: self._display.tabWidget.setCurrentIndex(1),
            ord('3'): lambda: self._display.tabWidget.setCurrentIndex(2),
            ord('4'): lambda: self._display.tabWidget.setCurrentIndex(3),
            # ord('G'): self._display.SetSelectionMode,
        }
        self.createCursors()

    def createCursors(self):
        module_pth = os.path.abspath(os.path.dirname(__file__))
        icon_pth = os.path.join(module_pth, "icons")

        _CURSOR_PIX_ROT = QtGui.QPixmap(os.path.join(icon_pth, "cursor-rotate.png"))
        _CURSOR_PIX_PAN = QtGui.QPixmap(os.path.join(icon_pth, "cursor-pan.png"))
        _CURSOR_PIX_ZOOM = QtGui.QPixmap(os.path.join(icon_pth, "cursor-magnify.png"))
        _CURSOR_PIX_ZOOM_AREA = QtGui.QPixmap(os.path.join(icon_pth, "cursor-magnify-area.png"))

        self._available_cursors = {
            "arrow": QtGui.QCursor(QtCore.Qt.ArrowCursor),  # default
            "cross": QtGui.QCursor(QtCore.Qt.CrossCursor),  # default
            "pan": QtGui.QCursor(_CURSOR_PIX_PAN),
            "rotate": QtGui.QCursor(_CURSOR_PIX_ROT),
            "zoom": QtGui.QCursor(_CURSOR_PIX_ZOOM),
            "zoom-area": QtGui.QCursor(_CURSOR_PIX_ZOOM_AREA),
        }

        self._current_cursor = "arrow"

    def keyPressEvent(self, event):
        code = event.key()
        if code in self._key_map:
            self._key_map[code]()
        # elif code in range(256):
        #     log.info('key: "%s"(code %i) not mapped to any function' % (chr(code), code))
        # else:
        #     log.info('key: code %i not mapped to any function' % code)

    def focusInEvent(self, event):
        if self._inited:
            self._display.Repaint()

    def focusOutEvent(self, event):
        if self._inited:
            self._display.Repaint()

    def paintEvent(self, event):
        if self._drawbox:
            if self._drawbox[2] == 0 or self._drawbox[3] == 0:
                return
            p1, p2, p3, p4 = self._drawbox[0], self._drawbox[1], self._drawbox[0] + self._drawbox[2], self._drawbox[1] + \
                             self._drawbox[3]
            pnt_2d_1 = [p1, p2]
            pnt_2d_2 = [p3, p2]
            pnt_2d_3 = [p3, p4]
            pnt_2d_4 = [p1, p4]
            pnt_3d_1 = self._display.View.ConvertWithProj(*pnt_2d_1)
            pnt_3d_2 = self._display.View.ConvertWithProj(*pnt_2d_2)
            pnt_3d_3 = self._display.View.ConvertWithProj(*pnt_2d_3)
            pnt_3d_4 = self._display.View.ConvertWithProj(*pnt_2d_4)
            P0 = gp_Pnt(pnt_3d_1[0], pnt_3d_1[1], pnt_3d_1[2])
            P1 = gp_Pnt(pnt_3d_2[0], pnt_3d_2[1], pnt_3d_2[2])
            P2 = gp_Pnt(pnt_3d_3[0], pnt_3d_3[1], pnt_3d_3[2])
            P3 = gp_Pnt(pnt_3d_4[0], pnt_3d_4[1], pnt_3d_4[2])
            aSegment1 = GC_MakeSegment(P0, P1)
            anEdge1 = BRepBuilderAPI_MakeEdge(aSegment1.Value())
            aWire1 = BRepBuilderAPI_MakeWire(anEdge1.Edge())
            aSegment2 = GC_MakeSegment(P1, P2)
            anEdge2 = BRepBuilderAPI_MakeEdge(aSegment2.Value())
            aWire2 = BRepBuilderAPI_MakeWire(anEdge2.Edge())
            aSegment3 = GC_MakeSegment(P2, P3)
            anEdge3 = BRepBuilderAPI_MakeEdge(aSegment3.Value())
            aWire3 = BRepBuilderAPI_MakeWire(anEdge3.Edge())
            aSegment4 = GC_MakeSegment(P3, P0)
            anEdge4 = BRepBuilderAPI_MakeEdge(aSegment4.Value())
            aWire4 = BRepBuilderAPI_MakeWire(anEdge4.Edge())
            aRectangle = BRepBuilderAPI_MakeWire(aWire1.Edge(), aWire2.Edge(), aWire3.Edge(), aWire4.Edge())
            if hasattr(self, 'ais_rect'):
                self._display.Context.Erase(self.ais_rect, False)
                self._display.Context.Remove(self.ais_rect, False)
            self.ais_rect = AIS_Shape(aRectangle.Shape())
            self.ais_rect.SetColor(rgb_color(1, 1, 0))
            self._display.Context.Display(self.ais_rect, False)
            self._display.Context.Deactivate(self.ais_rect)
            self._display.Context.UpdateCurrentViewer()

        # if self._drawbox:
        #     # self._display.Repaint()
        #     # self._display.Repaint()
        #     self._display.Context.UpdateCurrentViewer()
        #     self._display.Context.UpdateCurrentViewer()
        #     painter = QtGui.QPainter(self)
        #     # painter.setPen(QtGui.QPen(QtGui.QColor(1, 0, 0), 1))
        #     rect = QtCore.QRect(*self._drawbox)
        #     painter.drawRect(rect)

    def wheelEvent(self, event):
        try:  # PyQt4/PySide
            delta = event.delta()
        except:  # PyQt5
            delta = event.angleDelta().y()
        if delta > 0:
            zoom_factor = 1.1
        else:
            zoom_factor = 0.91
        self._display.ZoomFactor(zoom_factor)

    @property
    def cursor(self):
        return self._current_cursor

    @cursor.setter
    def cursor(self, value):
        if not self._current_cursor == value:

            self._current_cursor = value
            cursor = self._available_cursors.get(value)

            if cursor:
                self.qApp.setOverrideCursor(cursor)
            else:
                self.qApp.restoreOverrideCursor()

    def mousePressEvent(self, event):
        self.setFocus()
        ev = event.pos()
        self.dragStartPosX = ev.x()
        self.dragStartPosY = ev.y()
        self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)
        # 设置ais_manipulator
        if self.ais_manipulator:
            buttons = int(event.buttons())
            if buttons == QtCore.Qt.LeftButton:
                if self.ais_manipulator.ActiveMode() == 2:  # 2为旋转模式   只能旋转。  HasActiveMode（）
                    self.ais_manipulator.StartTransform(self.dragStartPosX, self.dragStartPosY,
                                                        self._display.View)
                    self.ais_manipulator_starting = True

        if hasattr(self, 'ais_rect'):
            self._display.Context.Erase(self.ais_rect, False)
            self._display.Context.Remove(self.ais_rect, False)
            self._display.Context.UpdateCurrentViewer()
            del self.ais_rect

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area and self._drawbox:
                [Xmin, Ymin, dx, dy] = self._drawbox
                if modifiers == QtCore.Qt.ShiftModifier:
                    self._display.ShiftSelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                else:
                    self._display.SelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._select_area = False
            elif self._zoom_area and self._drawbox:
                [Xmin, Ymin, dx, dy] = self._drawbox
                self._display.ZoomArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._zoom_area = False
            else:
                # multiple select if shift is pressed
                if modifiers == QtCore.Qt.ShiftModifier:
                    self._display.ShiftSelect(pt.x(), pt.y())
                else:
                    ##############################################
                    self._display.Select(pt.x(), pt.y())

                    # if (self._display.selected_shapes is not None) and HAVE_PYQT_SIGNAL:
                    #     self.sig_topods_selected.emit(self._display.selected_shapes)
                    #################################################
                    if self.dynamic_mease:
                        if self._display.Context.HasDetectedShape():
                            shp = self._display.Context.DetectedShape()
                            obj = self._display.Context.DetectedInteractive()
                            obj.owner = self._display.Context.DetectedOwner()
                        else:
                            shp = None
                            obj = None
                        self.dynamic_mease(pt.x(), pt.y(), click=True, shp=shp, obj=obj)

        if event.button() == QtCore.Qt.LeftButton and self.ais_manipulator_starting:
            self.ais_manipulator_starting = False
            self.ais_manipulator.StopTransform()
            # self.ais_manipulator.DeactivateCurrentMode()
            # self.ais_manipulator.SetModeActivationOnDetection(True)
            # self.ais_manipulator.SetModeActivationOnDetection(False)
            # self._display.Context.UpdateCurrentViewer()
        self.cursor = "arrow"
        if hasattr(self, 'ais_rect'):
            self._display.Context.Erase(self.ais_rect, False)
            self._display.Context.Remove(self.ais_rect, False)
            self._display.Context.UpdateCurrentViewer()
            del self.ais_rect

    def DrawBox(self, event):
        tolerance = 2
        pt = event.pos()
        dx = pt.x() - self.dragStartPosX
        dy = pt.y() - self.dragStartPosY
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return
        self._drawbox = [self.dragStartPosX, self.dragStartPosY, dx, dy]

    def mouseMoveEvent(self, evt):
        pt = evt.pos()
        buttons = int(evt.buttons())
        modifiers = evt.modifiers()
        # ROTATE  RightButton
        if buttons == QtCore.Qt.RightButton:
            # and not modifiers == QtCore.Qt.ShiftModifier):
            self.cursor = "rotate"
            self._display.Rotation(pt.x(), pt.y())
            self._drawbox = False
        # DYNAMIC ZOOM
        elif (buttons == QtCore.Qt.LeftButton and
              not modifiers == QtCore.Qt.ShiftModifier and
              int(modifiers) == QtCore.Qt.CTRL):
            self.cursor = "zoom"
            self._display.Repaint()
            start = self.dragStartPosX + self.dragStartPosY
            end = (pt.x() + pt.y())
            sep = int((end - start) / 2)
            self._display.DynamicZoom(0, 0, sep, 0)

            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self._drawbox = False
        # PAN
        elif buttons == QtCore.Qt.MidButton:
            dx = pt.x() - self.dragStartPosX
            dy = pt.y() - self.dragStartPosY
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self.cursor = "pan"
            self._display.Pan(dx, -dy)
            self._drawbox = False
        # DRAW BOX
        # ZOOM WINDOW
        elif (buttons == QtCore.Qt.LeftButton and
              # modifiers == QtCore.Qt.ShiftModifier):
              modifiers == QtCore.Qt.AltModifier):
            self._zoom_area = True
            self.cursor = "zoom-area"
            self.DrawBox(evt)
            self.update()
        # SELECT AREA
        elif (buttons == QtCore.Qt.LeftButton):
            if self.ais_manipulator_starting:
                if self.ais_manipulator.HasActiveMode():
                    if self.dxdydzAdjust:
                        next(self.dxdydzAdjust)
                    self.ais_manipulator.Transform(pt.x(), pt.y(),
                                                   self._display.View)
                    self._display.View.Redraw()
                    if self.dxdydzAdjust:
                        next(self.dxdydzAdjust)
            else:
                self._select_area = True
                self.DrawBox(evt)
                self.update()
        else:
            self._drawbox = False
            self._display.MoveTo(pt.x(), pt.y())
            # self.cursor = "arrow"
            if self.dynamic_mease:
                self.dynamic_mease(pt.x(), pt.y())

            if hasattr(self, 'ais_rect'):
                self._display.Context.Erase(self.ais_rect, False)
                self._display.Context.Remove(self.ais_rect, False)
                self._display.Context.UpdateCurrentViewer()
                del self.ais_rect