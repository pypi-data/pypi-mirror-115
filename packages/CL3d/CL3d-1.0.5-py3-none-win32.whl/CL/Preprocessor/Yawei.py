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
    last_AC = None
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
        if "YW_CIRCLE" in i:
            x = i.split('(')[1]
            x = x.split(',')[0]
            ncLine.GeoCenterX = float(x)
            y = i.split(',')[1]
            ncLine.GeoCenterY = float(y)
            z = i.split(',')[2]
            ncLine.GeoCenterZ = float(z)
            x1 = i.split(',')[3]
            dirX = float(x1)
            y1 = i.split(',')[4]
            dirY = float(y1)
            z1 = i.split(',')[5]
            dirZ = float(z1)
            dirX -= ncLine.GeoCenterX
            dirY -= ncLine.GeoCenterY
            dirZ -= ncLine.GeoCenterZ
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(dirX, dirY, dirZ)
            last = len(path) - 2  # 上上一行是切割起始点的位置
            dirX = path[last].X - ncLine.GeoCenterX
            dirY = path[last].Y - ncLine.GeoCenterY
            dirZ = path[last].Z - ncLine.GeoCenterZ
            ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Normalization(dirX, dirY, dirZ)

            ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z = Path.Path.Crossed(
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z],
                [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z]
            )
            r = i.split(',')[6]
            ncLine.GeoR = float(r)
            wl = i.split(',')[7]
            ncLine.MicroLink = float(wl)
            le = i.split(',')[8]
            ncLine.Lead = float(le)
            lk = i.split(',')[9].split(")")[0]
            ncLine.HoleCheck = bool(lk)
            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Circ = True
            ncLine.Geo = True
            ncLine.A = last_AC.A
            ncLine.C = last_AC.C
        if "YW_SLOT" in i:
            x = i.split('(')[1]
            x = x.split(',')[0]
            ncLine.GeoCenterX = float(x)
            y = i.split(',')[1]
            ncLine.GeoCenterY = float(y)
            z = i.split(',')[2]
            ncLine.GeoCenterZ = float(z)
            x1 = i.split(',')[3]
            dirX = float(x1)
            y1 = i.split(',')[4]
            dirY = float(y1)
            z1 = i.split(',')[5]
            dirZ = float(z1)
            dirX -= ncLine.GeoCenterX
            dirY -= ncLine.GeoCenterY
            dirZ -= ncLine.GeoCenterZ
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(dirX, dirY, dirZ)
            last = len(path) - 2  # 上上一行是切割起始点的位置
            dirX = path[last].X - ncLine.GeoCenterX
            dirY = path[last].Y - ncLine.GeoCenterY
            dirZ = path[last].Z - ncLine.GeoCenterZ
            ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Normalization(dirX, dirY, dirZ)

            ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z = Path.Path.Crossed(
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z],
                [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z]
            )
            w = i.split(',')[7]
            ncLine.GeoW = float(w)
            l = i.split(',')[6]
            ncLine.GeoL = float(l) + ncLine.GeoW

            wl = i.split(',')[8]
            ncLine.MicroLink = float(wl)
            le = i.split(',')[9]
            ncLine.Lead = float(le)
            lk = i.split(',')[10].split(")")[0]
            ncLine.HoleCheck = bool(lk)
            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Slot = True
            ncLine.Geo = True
            ncLine.A = last_AC.A
            ncLine.C = last_AC.C
        if "YW_RECT" in i:
            x = i.split('(')[1]
            x = x.split(',')[0]
            ncLine.GeoCenterX = float(x)
            y = i.split(',')[1]
            ncLine.GeoCenterY = float(y)
            z = i.split(',')[2]
            ncLine.GeoCenterZ = float(z)
            x1 = i.split(',')[3]
            dirX = float(x1)
            y1 = i.split(',')[4]
            dirY = float(y1)
            z1 = i.split(',')[5]
            dirZ = float(z1)
            dirX -= ncLine.GeoCenterX
            dirY -= ncLine.GeoCenterY
            dirZ -= ncLine.GeoCenterZ
            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(dirX, dirY, dirZ)
            last = len(path) - 2  # 上上一行是切割起始点的位置
            dirX = path[last].X - ncLine.GeoCenterX
            dirY = path[last].Y - ncLine.GeoCenterY
            dirZ = path[last].Z - ncLine.GeoCenterZ
            ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z = Path.Path.Normalization(dirX, dirY, dirZ)

            ncLine.GeoVectorX_X, ncLine.GeoVectorX_Y, ncLine.GeoVectorX_Z = Path.Path.Crossed(
                [ncLine.GeoVectorY_X, ncLine.GeoVectorY_Y, ncLine.GeoVectorY_Z],
                [ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z]
            )
            l = i.split(',')[6]
            ncLine.GeoL = float(l)
            w = i.split(',')[7]
            ncLine.GeoW = float(w)
            r = i.split(',')[8]
            ncLine.GeoR = float(r)
            wl = i.split(',')[9]
            ncLine.MicroLink = float(wl)
            le = i.split(',')[10]
            ncLine.Lead = float(le)
            lk = i.split(',')[11].split(")")[0]
            ncLine.HoleCheck = bool(lk)
            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Rect = True
            ncLine.Geo = True
            ncLine.A = last_AC.A
            ncLine.C = last_AC.C
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
        if "YW_APPROACH" in i:
            x = i.split('(')[1]
            x = x.split(',')[0]
            ncLine.X = float(x)
            y = i.split(',')[1]
            ncLine.Y = float(y)
            z = i.split(',')[2]
            z = z.split(')')[0]
            ncLine.Z = float(z)
            a = i.split(',')[3]
            ncLine.A = float(a)
            c = i.split(',')[4]
            c = c.split(')')[0]
            ncLine.C = float(c)
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

        ncLine.ID = ID
        ID += 1
        path.append(ncLine)
        if ncLine.A is not None:
            last_AC = ncLine
    # =========================
    return path


def update_Nc_List(paths):
    new_text_lsit = []
    preblock = None
    for block in paths:
        if block.Line:
            text = block.OriginText
            if "YW_APPROACH" not in text:
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
            else:
                if block.IsSameAsPrePoint:
                    string1 = '({},{},{},{},{})'.format(preblock_withX.X, preblock_withX.Y, preblock_withX.Z,
                                                        preblock_withX.A, preblock_withX.C)
                    text = re.sub(r'\([-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*\)', string1, text)
                else:
                    string1 = '({},{},{},{},{})'.format(block.X, block.Y, block.Z, block.A, block.C)
                    text = re.sub(r'\([-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*\)', string1, text)
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
            if block.Circ:  # N1160 HS_CIRC(13.000,2.000,0.000,2,"T1MsG1F5555")
                text = block.OriginText
                string1 = '({},{},{},{},{},{},{},{},{},{}'.format(block.GeoCenterX, block.GeoCenterY, block.GeoCenterZ,
                                                                  block.GeoCenterX + block.GeoVectorZ_X,
                                                                  block.GeoCenterY + block.GeoVectorZ_Y,
                                                                  block.GeoCenterZ + block.GeoVectorZ_Z,
                                                                  block.GeoR, block.MicroLink, block.Lead,
                                                                  int(block.HoleCheck))
                text = re.sub(
                    r'\([-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*\)',
                    string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Rect:  # N510 HS_RECT(18.120,4.060,0.000,2.000,0.000,2,"T1MsG1F0000")
                text = block.OriginText
                string1 = '({},{},{},{},{},{},{},{},{},{},{},{}'.format(block.GeoCenterX, block.GeoCenterY,
                                                                        block.GeoCenterZ,
                                                                        block.GeoCenterX + block.GeoVectorZ_X,
                                                                        block.GeoCenterY + block.GeoVectorZ_Y,
                                                                        block.GeoCenterZ + block.GeoVectorZ_Z,
                                                                        block.GeoL, block.GeoW,
                                                                        block.GeoR, block.MicroLink, block.Lead,
                                                                        int(block.HoleCheck))
                text = re.sub(
                    r'\([-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*\)',
                    string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
            elif block.Slot:  # HS_OBLONG(20.000,8.000,4.000,2.000,0.000,5,"T1MsG1F2222")
                text = block.OriginText
                string1 = '({},{},{},{},{},{},{},{},{},{},{}'.format(block.GeoCenterX, block.GeoCenterY,
                                                                     block.GeoCenterZ,
                                                                     block.GeoCenterX + block.GeoVectorZ_X,
                                                                     block.GeoCenterY + block.GeoVectorZ_Y,
                                                                     block.GeoCenterZ + block.GeoVectorZ_Z,
                                                                     block.GeoL - block.GeoW,
                                                                     block.GeoW, block.MicroLink, block.Lead,
                                                                     int(block.HoleCheck))
                text = re.sub(
                    r'\([-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*,[-]*\d*.\d*\)',
                    string1, text)
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
NC_FILE_FORMAT = 'YaWei NC File(*.mpf)'
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
