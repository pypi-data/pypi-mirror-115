from CL.Display.OCCViewer import rgb_color

from CL.lib import Path
import re
from OCC.Core.gp import gp_OX, gp_OZ
import os

def read_Nc_File(file):
    with open(file) as f:
        ncLines = f.readlines()
    path = []
    GCode = 0
    block = 1
    has_BLOCK_END = False
    ID = 0
    error_txt = ''
    try:
        for i in ncLines:
            error_txt = i
            ncLine = Path.Path()
            ncLine.OriginText = i
            if "LASER_ON" in i or "BEAM_ON" in i:
                GCode = 1
            if "LASER_OFF" in i or "BEAM_OFF" in i:
                GCode = 0
            if i[0] == "N":
                n = i.split()[0]
                n = n.split("N")[1]
                ncLine.N = n
            if "BLOCK_START" in i:
                n = i.split("BLOCK_START")[1]
                n = n.split()[0]
                if not has_BLOCK_END:
                    block = int(n)
            if "BLOCK_END" in i:
                block += 1
                has_BLOCK_END = True
            if "HS_CIRC" in i:  # N6170 HS_CIRC(19.940,2.000,0.000,0,0.000,1)
                last = len(path) - 1
                r1 = path[last].OriginText.split('R1=')[1].split()[0]
                r2 = path[last].OriginText.split('R2=')[1].split()[0]
                r3 = path[last].OriginText.split('R3=')[1].split()[0]
                r4 = path[last].OriginText.split('R4=')[1].split()[0]
                r5 = path[last].OriginText.split('R5=')[1].split()[0]
                r6 = path[last].OriginText.split('R6=')[1].split()[0]
                r7 = path[last].OriginText.split('R7=')[1].split()[0]
                r8 = path[last].OriginText.split('R8=')[1].split()[0]
                r9 = path[last].OriginText.split('R9=')[1].split()[0]
                r10 = path[last].OriginText.split('R10=')[1].split()[0]
                r11 = path[last].OriginText.split('R11=')[1].split()[0]
                # r12 = path[last].OriginText.split('R12=')[1].split()[0]
                ncLine.GeoCenterX = float(r1)
                ncLine.GeoCenterY = float(r2)
                ncLine.GeoCenterZ = float(r3)
                ncLine.A = float(r4)
                ncLine.C = float(r5)
                ncLine.GeoVectorZ_X = float(r6)
                ncLine.GeoVectorZ_Y = float(r7)
                ncLine.GeoVectorZ_Z = float(r8)
                ncLine.GeoVectorX_X = float(r9)
                ncLine.GeoVectorX_Y = float(r10)
                ncLine.GeoVectorX_Z = float(r11)
                ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Crossed(
                    [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z],
                    [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z]
                )

                r = i.split('(')[1]
                r = r.split(',')[0]
                ncLine.GeoR = float(r) / 2
                le = i.split(',')[1]
                ncLine.GeoMD = float(le)
                le = i.split(',')[2]
                ncLine.GeoMR = float(le)

                ncLine.GType = 1
                ncLine.BlockNum = block
                ncLine.Circ = True
                ncLine.Geo = True
            if "HS_OBLONG" in i:
                last = len(path) - 1
                r1 = path[last].OriginText.split('R1=')[1].split()[0]
                r2 = path[last].OriginText.split('R2=')[1].split()[0]
                r3 = path[last].OriginText.split('R3=')[1].split()[0]
                r4 = path[last].OriginText.split('R4=')[1].split()[0]
                r5 = path[last].OriginText.split('R5=')[1].split()[0]
                r6 = path[last].OriginText.split('R6=')[1].split()[0]
                r7 = path[last].OriginText.split('R7=')[1].split()[0]
                r8 = path[last].OriginText.split('R8=')[1].split()[0]
                r9 = path[last].OriginText.split('R9=')[1].split()[0]
                r10 = path[last].OriginText.split('R10=')[1].split()[0]
                r11 = path[last].OriginText.split('R11=')[1].split()[0]
                # r12 = path[last].OriginText.split('R12=')[1].split()[0]
                ncLine.GeoCenterX = float(r1)
                ncLine.GeoCenterY = float(r2)
                ncLine.GeoCenterZ = float(r3)
                ncLine.A = float(r4)
                ncLine.C = float(r5)
                ncLine.GeoVectorZ_X = float(r6)
                ncLine.GeoVectorZ_Y = float(r7)
                ncLine.GeoVectorZ_Z = float(r8)
                ncLine.GeoVectorX_X = float(r9)
                ncLine.GeoVectorX_Y = float(r10)
                ncLine.GeoVectorX_Z = float(r11)
                ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Crossed(
                    [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z],
                    [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z]
                )

                r = i.split('(')[1]
                r = r.split(',')[0]
                ncLine.GeoL = float(r)
                le = i.split(',')[1]
                ncLine.GeoW = float(le)
                le = i.split(',')[3]
                ncLine.GeoMD = float(le)
                le = i.split(',')[4]
                ncLine.GeoMR = float(le)

                ncLine.GType = 1
                ncLine.BlockNum = block
                ncLine.Slot = True
                ncLine.Geo = True
            if "HS_RECT" in i:
                last = len(path) - 1
                r1 = path[last].OriginText.split('R1=')[1].split()[0]
                r2 = path[last].OriginText.split('R2=')[1].split()[0]
                r3 = path[last].OriginText.split('R3=')[1].split()[0]
                r4 = path[last].OriginText.split('R4=')[1].split()[0]
                r5 = path[last].OriginText.split('R5=')[1].split()[0]
                r6 = path[last].OriginText.split('R6=')[1].split()[0]
                r7 = path[last].OriginText.split('R7=')[1].split()[0]
                r8 = path[last].OriginText.split('R8=')[1].split()[0]
                r9 = path[last].OriginText.split('R9=')[1].split()[0]
                r10 = path[last].OriginText.split('R10=')[1].split()[0]
                r11 = path[last].OriginText.split('R11=')[1].split()[0]
                # r12 = path[last].OriginText.split('R12=')[1].split()[0]
                ncLine.GeoCenterX = float(r1)
                ncLine.GeoCenterY = float(r2)
                ncLine.GeoCenterZ = float(r3)
                ncLine.A = float(r4)
                ncLine.C = float(r5)
                ncLine.GeoVectorZ_X = float(r6)
                ncLine.GeoVectorZ_Y = float(r7)
                ncLine.GeoVectorZ_Z = float(r8)
                ncLine.GeoVectorX_X = float(r9)
                ncLine.GeoVectorX_Y = float(r10)
                ncLine.GeoVectorX_Z = float(r11)
                ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Crossed(
                    [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z],
                    [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z]
                )

                r = i.split('(')[1]
                r = r.split(',')[0]
                ncLine.GeoL = float(r)
                le = i.split(',')[1]
                ncLine.GeoW = float(le)
                le = i.split(',')[2]
                ncLine.GeoR = float(le)
                le = i.split(',')[3]
                ncLine.GeoMD = float(le)
                le = i.split(',')[4]
                ncLine.GeoMR = float(le)

                ncLine.GType = 1
                ncLine.BlockNum = block
                ncLine.Rect = True
                ncLine.Geo = True
            if "G00 X=" in i or "G01 X=" in i:
                if 'X=' in i:
                    ncLine.X = float(i.split('X=')[1].split()[0])
                if 'Y=' in i:
                    ncLine.Y = float(i.split('Y=')[1].split()[0])
                if 'Z=' in i:
                    ncLine.Z = float(i.split('Z=')[1].split()[0])
                if 'A=' in i:
                    ncLine.A = float(i.split('A=')[1].split()[0])
                if 'C=' in i:
                    ncLine.C = float(i.split('C=')[1].split()[0])
                if 'F' in i:
                    ncLine.F = float(i.split('F')[1].split()[0])
                ncLine.GType = GCode
                ncLine.BlockNum = block
                ncLine.Line = True
            if "CIP I1=" in i:
                if 'F' in i:
                    ncLine.F = float(i.split('F')[1].split()[0])
                ncLine.X = float(i.split('X=')[1].split()[0])
                ncLine.Y = float(i.split('Y=')[1].split()[0])
                ncLine.Z = float(i.split('Z=')[1].split()[0])
                ncLine.I = float(i.split('I1=')[1].split()[0])
                ncLine.J = float(i.split('J1=')[1].split()[0])
                ncLine.K = float(i.split('K1=')[1].split()[0])
                ncLine.A = float(i.split('A=')[1].split()[0])
                ncLine.C = float(i.split('C=')[1].split()[0])

                ncLine.GType = GCode
                ncLine.BlockNum = block
                ncLine.Cip = True

            ncLine.BlockNum = block

            ncLine.ID = ID
            ID += 1
            path.append(ncLine)
        # =========================
        return path
    except:
        raise BaseException(error_txt)



def update_R1_12(block, text):
    # N610 R1=2220.0530899 R2=1006.0281918 R3=-257.4650127 R4=77.14667 R5=14.10727 R6=0.237612 R7=-0.945544 R8=0.222456 R9=-0.964724 R10=-0.202993 R11=0.167635 R12=0.0
    strint1 = 'R1={} R2={} R3={} R4={} R5={} R6={} R7={} R8={} R9={} R10={} R11={} R12=0.0'.format(
        round(block.GeoCenterX, 3),
        round(block.GeoCenterY, 3),
        round(block.GeoCenterZ, 3),
        round(block.A, 3), round(block.C, 3),
        round(block.GeoVectorZ_X, 3),
        round(block.GeoVectorZ_Y, 3),
        round(block.GeoVectorZ_Z, 3),
        round(block.GeoVectorX_X, 3),
        round(block.GeoVectorX_Y, 3),
        round(block.GeoVectorX_Z, 3))
    return re.sub(r'R1=.*', strint1, text)


def update_Nc_List(paths):
    new_text_lsit = []
    preblock = None
    for block in paths:
        if block.Line:
            text = block.OriginText
            if block.IsSameAsPrePoint:
                text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(round(preblock_withX.X, 3)), text)
                text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(round(preblock_withX.Y, 3)), text)
                text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(round(preblock_withX.Z, 3)), text)
                text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(round(preblock_withX.A, 3)), text)
                text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(round(preblock_withX.C, 3)), text)
            else:
                text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(round(block.X, 3)), text)
                text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(round(block.Y, 3)), text)
                if block.Z:
                    text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(round(block.Z, 3)), text)
                text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(round(block.A, 3)), text)
                text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(round(block.C, 3)), text)
            block.EditedText = text
            new_text_lsit.append(text)
        elif block.Cip:
            text = block.OriginText
            text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(round(block.X, 3)), text)
            text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(round(block.Y, 3)), text)
            text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(round(block.Z, 3)), text)
            text = re.sub(r'I1=[-]*\d*.\d*', 'I1={}'.format(round(block.I, 3)), text)
            text = re.sub(r'J1=[-]*\d*.\d*', 'J1={}'.format(round(block.J, 3)), text)
            text = re.sub(r'K1=[-]*\d*.\d*', 'K1={}'.format(round(block.K, 3)), text)
            text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(round(block.A, 3)), text)
            text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(round(block.C, 3)), text)
            block.EditedText = text
            new_text_lsit.append(text)
        elif block.Geo:
            if block.Circ:  # N1160 HS_CIRC(13.000,2.000,0.000,2,"T1MsG1F5555")
                new_text_lsit[-1] = update_R1_12(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                text = block.OriginText
                string1 = '({},{},{}'.format(round(block.GeoR * 2, 3), round(block.GeoMD, 3), round(block.GeoMR, 3))
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Rect:  # N510 HS_RECT(18.120,4.060,0.000,2.000,0.000,2,"T1MsG1F0000")
                new_text_lsit[-1] = update_R1_12(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                text = block.OriginText
                string1 = '({},{},{},{},{}'.format(round(block.GeoL, 3), round(block.GeoW, 3), round(block.GeoR, 3),
                                                   round(block.GeoMD, 3), round(block.GeoMR, 3))
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Slot:  # HS_OBLONG(20.000,8.000,4.000,2.000,0.000,5,"T1MsG1F2222")
                new_text_lsit[-1] = update_R1_12(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                text = block.OriginText
                string1 = '({},{},{},{},{}'.format(round(block.GeoL, 3), round(block.GeoW, 3), round(block.GeoW / 2, 3),
                                                   round(block.GeoMD, 3), round(block.GeoMR, 3))
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            else:
                new_text_lsit.append(block.OriginText)
        else:
            new_text_lsit.append(block.OriginText)
        preblock = block
        if block.X is not None:
            preblock_withX = block
    return new_text_lsit


# 文件打开时，显示的后缀过滤器
NC_FILE_FORMAT = 'DaZu NC File(*.mpf)'
# 处理nc文件函数
READ_NC_FILE = read_Nc_File
# 更新NC文件
UPDATE_NC_LIST = update_Nc_List
# A轴旋转点Z值高度
A_CENTER_Z = 278.398
# 喷嘴高度
HEAD_HEIGHT = 2.0

A_AIX1 = gp_OX()
C_AIX1 = gp_OZ()


A_MODEL = os.path.join(os.path.dirname(__file__), 'dazu_a.brep')
C_MODEL = os.path.join(os.path.dirname(__file__), 'dazu_c.brep')

A_NAME = 'A'
C_NAME = 'C'

COLOR = rgb_color(0.55, 0.55, 0.55)
