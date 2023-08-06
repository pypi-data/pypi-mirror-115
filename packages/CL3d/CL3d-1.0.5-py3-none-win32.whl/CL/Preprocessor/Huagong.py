from CL.lib import Path
import re
from OCC.Core.gp import gp_OX, gp_OZ


def read_Nc_File(file):
    with open(file) as f:
        ncLines = f.readlines()
    path = []
    GCode = 0
    block = 1
    has_BLOCK_END = False
    ID = 0
    for i in ncLines:
        ncLine = Path.Path()
        ncLine.OriginText = i
        if "BEAMON" in i or "BEAM_ON" in i:
            GCode = 1
        if "BEAMOFF" in i or "BEAM_OFF" in i:
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
        if "HG_CIRC" in i and "EXTERN" not in i:  #
            last = len(path)
            r1 = path[last - 2].OriginText.split('R80=')[1].split()[0]
            r2 = path[last - 2].OriginText.split('R81=')[1].split()[0]
            r3 = path[last - 2].OriginText.split('R82=')[1].split()[0]
            r4 = path[last - 2].OriginText.split('R83=')[1].split()[0]
            r5 = path[last - 2].OriginText.split('R84=')[1].split()[0]
            r6 = path[last - 1].OriginText.split('R85=')[1].split()[0]
            r7 = path[last - 1].OriginText.split('R86=')[1].split()[0]
            r8 = path[last - 1].OriginText.split('R87=')[1].split()[0]
            r9 = path[last - 1].OriginText.split('R88=')[1].split()[0]
            r10 = path[last - 1].OriginText.split('R89=')[1].split()[0]
            r11 = path[last - 1].OriginText.split('R90=')[1].split()[0]
            ncLine.GeoCenterX = float(r1)
            ncLine.GeoCenterY = float(r2)
            ncLine.GeoCenterZ = float(r3)
            ncLine.A = float(r4)
            ncLine.C = float(r5)
            ncLine.GeoVectorY_X = float(r6)
            ncLine.GeoVectorY_Y = float(r7)
            ncLine.GeoVectorY_Z = float(r8)
            ncLine.GeoVectorX_X = float(r9)
            ncLine.GeoVectorX_Y = float(r10)
            ncLine.GeoVectorX_Z = float(r11)
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Crossed(
                [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z],
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z]
            )

            r = i.split('(')[1]
            r = r.split(',')[0]
            ncLine.GeoR = float(r)
            le = i.split(',')[1]
            ncLine.GeoMD = float(le)
            le = i.split(',')[2].split(')')[0]
            ncLine.GeoMR = float(le)

            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Circ = True
            ncLine.Geo = True
        if "HG_SLOT" in i and "EXTERN" not in i:
            last = len(path)
            r1 = path[last - 2].OriginText.split('R80=')[1].split()[0]
            r2 = path[last - 2].OriginText.split('R81=')[1].split()[0]
            r3 = path[last - 2].OriginText.split('R82=')[1].split()[0]
            r4 = path[last - 2].OriginText.split('R83=')[1].split()[0]
            r5 = path[last - 2].OriginText.split('R84=')[1].split()[0]
            r6 = path[last - 1].OriginText.split('R85=')[1].split()[0]
            r7 = path[last - 1].OriginText.split('R86=')[1].split()[0]
            r8 = path[last - 1].OriginText.split('R87=')[1].split()[0]
            r9 = path[last - 1].OriginText.split('R88=')[1].split()[0]
            r10 = path[last - 1].OriginText.split('R89=')[1].split()[0]
            r11 = path[last - 1].OriginText.split('R90=')[1].split()[0]
            ncLine.GeoCenterX = float(r1)
            ncLine.GeoCenterY = float(r2)
            ncLine.GeoCenterZ = float(r3)
            ncLine.A = float(r4)
            ncLine.C = float(r5)
            ncLine.GeoVectorY_X = float(r6)
            ncLine.GeoVectorY_Y = float(r7)
            ncLine.GeoVectorY_Z = float(r8)
            ncLine.GeoVectorX_X = float(r9)
            ncLine.GeoVectorX_Y = float(r10)
            ncLine.GeoVectorX_Z = float(r11)
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Crossed(
                [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z],
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z]
            )

            r = i.split('(')[1]
            r = r.split(',')[0]
            ncLine.GeoL = float(r)
            le = i.split(',')[1]
            ncLine.GeoW = float(le)
            le = i.split(',')[2]
            ncLine.GeoMD = float(le)
            le = i.split(',')[3].split(')')[0]
            ncLine.GeoMR = float(le)

            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Slot = True
            ncLine.Geo = True
        if "HG_RECT" in i and "EXTERN" not in i:
            last = len(path)
            r1 = path[last - 2].OriginText.split('R80=')[1].split()[0]
            r2 = path[last - 2].OriginText.split('R81=')[1].split()[0]
            r3 = path[last - 2].OriginText.split('R82=')[1].split()[0]
            r4 = path[last - 2].OriginText.split('R83=')[1].split()[0]
            r5 = path[last - 2].OriginText.split('R84=')[1].split()[0]
            r6 = path[last - 1].OriginText.split('R85=')[1].split()[0]
            r7 = path[last - 1].OriginText.split('R86=')[1].split()[0]
            r8 = path[last - 1].OriginText.split('R87=')[1].split()[0]
            r9 = path[last - 1].OriginText.split('R88=')[1].split()[0]
            r10 = path[last - 1].OriginText.split('R89=')[1].split()[0]
            r11 = path[last - 1].OriginText.split('R90=')[1].split()[0]
            ncLine.GeoCenterX = float(r1)
            ncLine.GeoCenterY = float(r2)
            ncLine.GeoCenterZ = float(r3)
            ncLine.A = float(r4)
            ncLine.C = float(r5)
            ncLine.GeoVectorY_X = float(r6)
            ncLine.GeoVectorY_Y = float(r7)
            ncLine.GeoVectorY_Z = float(r8)
            ncLine.GeoVectorX_X = float(r9)
            ncLine.GeoVectorX_Y = float(r10)
            ncLine.GeoVectorX_Z = float(r11)
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Crossed(
                [ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z],
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z]
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
            le = i.split(',')[4].split(')')[0]
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


def update_R80_84(block, text):
    strint1 = 'R80={} R81={} R82={} R83={} R84={}'.format(block.GeoCenterX,
                                                          block.GeoCenterY,
                                                          block.GeoCenterZ,
                                                          block.A, block.C)
    return re.sub(r'R80=.*', strint1, text)


def update_R85_90(block, text):
    strint1 = 'R85={} R86={} R87={} R88={} R89={} R90={}'.format(block.GeoVectorY_X,
                                                                 block.GeoVectorY_Y,
                                                                 block.GeoVectorY_Z,
                                                                 block.GeoVectorX_X,
                                                                 block.GeoVectorX_Y,
                                                                 block.GeoVectorX_Z)
    return re.sub(r'R85=.*', strint1, text)


def update_Nc_List(paths):
    new_text_lsit = []
    preblock = None
    last_preblock = None
    for block in paths:
        if block.Line:
            text = block.OriginText
            if block.IsSameAsPrePoint:
                text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(preblock_withX.X), text)
                text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(preblock_withX.Y), text)
                text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(preblock_withX.Z), text)
                text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(preblock_withX.A), text)
                text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(preblock_withX.C), text)
            else:
                text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(block.X), text)
                text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(block.Y), text)
                text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(block.Z), text)
                text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(block.A), text)
                text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(block.C), text)
            block.EditedText = text
            new_text_lsit.append(text)
        elif block.Cip:
            text = block.OriginText
            text = re.sub(r'X=[-]*\d*.\d*', 'X={}'.format(block.X), text)
            text = re.sub(r'Y=[-]*\d*.\d*', 'Y={}'.format(block.Y), text)
            text = re.sub(r'Z=[-]*\d*.\d*', 'Z={}'.format(block.Z), text)
            text = re.sub(r'I1=[-]*\d*.\d*', 'I1={}'.format(block.I), text)
            text = re.sub(r'J1=[-]*\d*.\d*', 'J1={}'.format(block.J), text)
            text = re.sub(r'K1=[-]*\d*.\d*', 'K1={}'.format(block.K), text)
            text = re.sub(r'A=[-]*\d*.\d*', 'A={}'.format(block.A), text)
            text = re.sub(r'C=[-]*\d*.\d*', 'C={}'.format(block.C), text)
            block.EditedText = text
            new_text_lsit.append(text)
        elif block.Geo:
            if block.Circ:
                new_text_lsit[-2] = update_R80_84(block, new_text_lsit[-2])
                new_text_lsit[-1] = update_R85_90(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                last_preblock.EditedText = new_text_lsit[-2]
                text = block.OriginText
                string1 = '({},{},{}'.format(block.GeoR, block.GeoMD, block.GeoMR)
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Rect:
                new_text_lsit[-2] = update_R80_84(block, new_text_lsit[-2])
                new_text_lsit[-1] = update_R85_90(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                last_preblock.EditedText = new_text_lsit[-2]
                text = block.OriginText
                string1 = '({},{},{},{},{}'.format(block.GeoL, block.GeoW, block.GeoR, block.GeoMD, block.GeoMR)
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Slot:
                new_text_lsit[-2] = update_R80_84(block, new_text_lsit[-2])
                new_text_lsit[-1] = update_R85_90(block, new_text_lsit[-1])
                preblock.EditedText = new_text_lsit[-1]
                last_preblock.EditedText = new_text_lsit[-2]
                text = block.OriginText
                string1 = '({},{},{},{}'.format(block.GeoL, block.GeoW, block.GeoMD, block.GeoMR)
                text = re.sub(r'\(\d*.\d*,\d*.\d*,\d*.\d*,\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            else:
                new_text_lsit.append(block.OriginText)
        else:
            new_text_lsit.append(block.OriginText)
        last_preblock = preblock
        preblock = block
        if block.X is not None:
            preblock_withX = block
    return new_text_lsit


# 文件打开时，显示的后缀过滤器
NC_FILE_FORMAT = 'HuaGong NC File(*.mpf)'
# 处理nc文件函数
READ_NC_FILE = read_Nc_File
# 更新NC文件
UPDATE_NC_LIST = update_Nc_List
# A轴旋转点Z值高度
A_CENTER_Z = 271.45
# 喷嘴高度
HEAD_HEIGHT = 2.0

A_AIX1 = gp_OX()
C_AIX1 = gp_OZ()

A_MODEL = './Preprocessor/yawei_a.brep'
C_MODEL = './Preprocessor/yawei_c.brep'
