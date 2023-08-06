from CL.lib import Action
from CL.lib import Base
from CL.lib import Check
from CL.lib import Editor
from CL.lib import Editor2
from CL.lib import Editor_Add_Point
from CL.lib import Editor_Del_Point
from CL.lib import Editor_Move
from CL.lib import Editor_Rotate
from CL.lib import File
from CL.lib import Filter
from CL.lib import Menu
from CL.lib import Path
from CL.lib import Simulation
from CL.lib import View
from CL.lib import Editor_Edge
from CL.lib import Syn_sim
from CL.lib import Modify_AC

from ecdsa import SECP256k1, VerifyingKey
import wmi
from CL.ui import all_UI
import CL.Preprocessor
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Dir
from OCC.Extend.ShapeFactory import make_edge
from OCC.Core.Geom import Geom_Line, Geom_Circle
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from CL.Display.OCCViewer import rgb_color
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.Aspect import Aspect_TOM_BALL, Aspect_TOM_PLUS
from OCC.Core.Prs3d import Prs3d_PointAspect
from OCC.Core.BRep import BRep_Tool_Curve
from OCC.Core.Quantity import Quantity_Color

from OCC.Core.AIS import AIS_Trihedron
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.gp import gp_Pnt, gp_Dir
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape, BRepExtrema_ExtPC

from OCC.Core.AIS import AIS_Manipulator, AIS_Shape, AIS_Trihedron
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax3, gp_Ax1, gp_XYZ, gp_Vec
from CL.Display.OCCViewer import rgb_color
from OCC.Core.Geom import Geom_Transformation
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.Geom import Geom_Axis2Placement
from OCC.Core.BRep import BRep_Tool_Curve, BRep_Tool_Pnt
from OCC.Core.TopExp import topexp_FirstVertex, topexp_LastVertex
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire)
from OCC.Core.BRepTools import BRepTools_WireExplorer

from OCC.Core.AIS import AIS_Shape, AIS_InteractiveObject, AIS_Manipulator
from OCC.Core.BRepTools import BRepTools_WireExplorer
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax3
from OCC.Core.BRep import BRep_Tool_Curve, BRep_Tool_Pnt
from OCC.Core.TopExp import topexp_FirstVertex, topexp_LastVertex
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire)

from OCC.Core.Geom import Geom_Line
from OCC.Core.AIS import AIS_InteractiveObject, AIS_Shape
from OCC.Extend.ShapeFactory import make_edge, make_wire, make_vertex
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Vec
from OCC.Core.BRep import BRep_Tool_Curve, BRep_Tool_Pnt
from OCC.Core.TopExp import topexp_LastVertex
from OCC.Core.TopoDS import TopoDS_Edge
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BOPAlgo import BOPAlgo_Splitter
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepGProp import brepgprop_LinearProperties
from OCC.Core.GProp import GProp_GProps

from OCC.Core.AIS import AIS_InteractiveObject, AIS_Shape
from OCC.Extend.ShapeFactory import make_edge, make_wire
from OCC.Core.BRep import BRep_Tool_Pnt
from OCC.Core.TopExp import topexp_FirstVertex, topexp_LastVertex
from OCC.Core.TopoDS import TopoDS_Vertex
from OCC.Extend.TopologyUtils import TopologyExplorer

from OCC.Core.AIS import AIS_Shape, AIS_Manipulator
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax3
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add

from OCC.Core.Geom import Geom_Transformation
from OCC.Core.AIS import AIS_Shape
from OCC.Extend.ShapeFactory import make_edge, make_vertex
from CL.Display.OCCViewer import rgb_color
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax1, gp_Vec, gp_DX, gp_DY, gp_DZ, gp_Pln
from OCC.Core.BRep import BRep_Tool_Pnt
from OCC.Core.TopoDS import TopoDS_Vertex
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.ProjLib import projlib
from OCC.Core.ElSLib import elslib

from OCC.Extend.DataExchange import write_iges_file

from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir

from OCC.Core.AIS import AIS_Shape
from OCC.Extend.ShapeFactory import make_edge
from OCC.Core.gp import gp_Trsf, gp_Pnt, gp_Dir, gp_Ax2, gp_Ax3, gp_Circ, gp_Vec, gp_Origin, gp_OX, gp_OZ
from OCC.Core.BRep import BRep_Tool_Curve
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.GeomAdaptor import GeomAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_UniformAbscissa

from OCC.Core.AIS import AIS_Shaded, AIS_WireFrame


