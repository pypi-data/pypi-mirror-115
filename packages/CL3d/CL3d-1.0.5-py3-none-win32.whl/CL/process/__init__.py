
from OCC.Core.gp import (gp_Pnt, gp_Vec, gp_Trsf, gp_Ax2, gp_Ax3,
                         gp_Dir, gp_Circ)
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire)
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Graphic3d import Graphic3d_ZLayerSettings
from CL.Display.OCCViewer import rgb_color
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Core.BRep import BRep_Tool_Curve, BRep_Tool_Pnt
from OCC.Core.TopExp import topexp_FirstVertex, topexp_LastVertex
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire)
from OCC.Core.BRepTools import BRepTools_WireExplorer
from CL.process import MakeShape, RapidFeedUpdate