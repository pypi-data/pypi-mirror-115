

from __future__ import print_function

import random
import os
import os.path
import sys

from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from CL.Display.SimpleGui import init_display

from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.BRepTools import breptools_Read, breptools_Write

def import_as_one_shape(event=None):
    shp = read_step_file(os.path.join('.', 'yawei-a.stp'))
    shp2 = read_step_file(os.path.join('.', 'yawei-c.stp'))
    display.EraseAll()
    display.DisplayShape(shp, update=True)
    display.DisplayShape(shp2, update=True)
    breptools_Write(shp, './yawei_a.brep')
    breptools_Write(shp2, './yawei_c.brep')

def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    add_menu('STEP import')
    add_function_to_menu('STEP import', import_as_one_shape)
    start_display()
