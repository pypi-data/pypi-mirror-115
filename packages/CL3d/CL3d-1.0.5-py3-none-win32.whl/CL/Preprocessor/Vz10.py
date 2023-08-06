from CL.lib import Path
import re
from OCC.Core.gp import gp_Ax1, gp_Origin, gp_Dir, gp_Vec, gp_Quaternion


def read_Nc_File(file):
    with open(file) as f:
        ncLines = f.readlines()
    path = []
    GCode = 0
    block = 1
    has_BLOCK_END = False
    ID = 0
    CIP = None
    GEO = None
    circ = False
    for i in ncLines:
        ncLine = Path.Path()
        ncLine.OriginText = i
        ncLine.BlockNum = block
        if "M120" in i or "M188" in i:
            GCode = 1
        if "M121" in i or "M189" in i:
            GCode = 0
        if i[0] == "N":
            n = re.split(r'\D', i)[1]
            ncLine.N = n

        if "G8.1X" in i and not GEO:
            if 'X' in i:
                T = i.split('X')[1]
                x = re.split(r'[A-Z]', T)[0]
                ncLine.X = float(x)
            if 'Y' in i:
                T = i.split('Y')[1]
                y = re.split(r'[A-Z]', T)[0]
                ncLine.Y = float(y)
            if 'Z' in i:
                T = i.split('Z')[1]
                z = re.split(r'[A-Z]', T)[0]
                ncLine.Z = float(z)
            if 'W' in i:
                T = i.split('W')[1]
                w = re.split(r'[A-Z]', T)[0]
                ncLine.C = float(w)
            if 'U' in i:
                T = i.split('U')[1]
                u = re.split(r'[A-Z]', T)[0]
                ncLine.A = float(u)
            if 'F' in i:
                ncLine.F = i.split('F')[1].split()[0]
            ncLine.GType = GCode
            ncLine.BlockNum = block
            ncLine.Line = True
        if "G8.5X" in i and not GEO:
            if not CIP:
                CIP = ncLine
                T = i.split('X')[1]
                x = re.split(r'[A-Z]', T)[0]
                CIP.I = float(x)

                T = i.split('Y')[1]
                y = re.split(r'[A-Z]', T)[0]
                CIP.J = float(y)

                T = i.split('Z')[1]
                z = re.split(r'[A-Z]', T)[0]
                CIP.K = float(z)

                CIP.OriginTextIJK = i
                CIP.GType = GCode
                CIP.BlockNum = block
                CIP.Cip = True
                continue
            else:
                T = i.split('X')[1]
                x = re.split(r'[A-Z]', T)[0]
                CIP.X = float(x)

                T = i.split('Y')[1]
                y = re.split(r'[A-Z]', T)[0]
                CIP.Y = float(y)

                T = i.split('Z')[1]
                z = re.split(r'[A-Z]', T)[0]
                CIP.Z = float(z)

                T = i.split('W')[1]
                w = re.split(r'[A-Z]', T)[0]
                CIP.C = float(w)

                T = i.split('U')[1]
                u = re.split(r'[A-Z]', T)[0]
                CIP.A = float(u)

                CIP.OriginTextXYZ = i
                ncLine = CIP
                CIP = None


        if "(X" in i and GEO:   # (X266.576Y132.788Z-15.065)
            yx = i.split('X')[1]
            yx = yx.split('Y')[0]
            yx = float(yx)

            yy = i.split('Y')[1]
            yy = yy.split('Z')[0]
            yy = float(yy)

            yz = i.split('Z')[1]
            yz = yz.split(')')[0]
            yz = float(yz)

            GEO.GeoVectorY_X, GEO.GeoVectorY_Y, GEO.GeoVectorY_Z = Path.Path.Normalization(
                yx - GEO.GeoCenterX,
                yy - GEO.GeoCenterY,
                yz - GEO.GeoCenterZ
            )
            GEO.GeoVectorX_X, GEO.GeoVectorX_Y, GEO.GeoVectorX_Z = Path.Path.Crossed(
                [GEO.GeoVectorY_X, GEO.GeoVectorY_Y, GEO.GeoVectorY_Z],
                [GEO.GeoVectorZ_X, GEO.GeoVectorZ_Y, GEO.GeoVectorZ_Z]
            )
            ncLine = GEO
            GEO = None
            block += 1
            circ = False

        if circ:
            raise

        if "G65.1P9323" in i:  # N00075G65.1P9323I13.000Q2.00
            last = len(path) - 1
            ncLine.GeoCenterX = path[last].X
            ncLine.GeoCenterY = path[last].Y
            ncLine.GeoCenterZ = path[last].Z
            ncLine.A = path[last].A
            ncLine.C = path[last].C

            Lx = path[last - 1].X
            Ly = path[last - 1].Y
            Lz = path[last - 1].Z

            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(
                Lx - ncLine.GeoCenterX,
                Ly - ncLine.GeoCenterY,
                Lz - ncLine.GeoCenterZ
            )

            r = i.split('I')[1]
            r = r.split('Q')[0]
            ncLine.GeoR = float(r) / 2
            le = i.split('Q')[1]
            le = re.split(r'[A-Z]', le)[0]
            ncLine.GeoMD = float(le)

            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Circ = True
            ncLine.Geo = True
            GEO = ncLine
            circ = True
            continue

        if GEO:   # X1099.712Y306.284Z-109.456W-106.475U63.758
            if GEO.Rect or GEO.Slot:
                yx = i.split('X')[1]
                yx = yx.split('Y')[0]
                yx = float(yx)

                yy = i.split('Y')[1]
                yy = yy.split('Z')[0]
                yy = float(yy)

                yz = i.split('Z')[1]
                yz = yz.split('W')[0]
                yz = float(yz)

                GEO.GeoVectorX_X, GEO.GeoVectorX_Y, GEO.GeoVectorX_Z = Path.Path.Normalization(
                    yx - GEO.GeoCenterX,
                    yy - GEO.GeoCenterY,
                    yz - GEO.GeoCenterZ
                )
                GEO.GeoVectorY_X, GEO.GeoVectorY_Y, GEO.GeoVectorY_Z = Path.Path.Crossed(
                    [GEO.GeoVectorZ_X, GEO.GeoVectorZ_Y, GEO.GeoVectorZ_Z],
                    [GEO.GeoVectorX_X, GEO.GeoVectorX_Y, GEO.GeoVectorX_Z]
                )
                GEO.VX_TEXT = i
                ncLine = GEO
                GEO = None
                block += 1
        if "G65.1P9324" in i:
            last = len(path) - 1
            ncLine.GeoCenterX = path[last].X
            ncLine.GeoCenterY = path[last].Y
            ncLine.GeoCenterZ = path[last].Z
            ncLine.A = path[last].A
            ncLine.C = path[last].C

            Lx = path[last - 1].X
            Ly = path[last - 1].Y
            Lz = path[last - 1].Z

            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(
                Lx - ncLine.GeoCenterX,
                Ly - ncLine.GeoCenterY,
                Lz - ncLine.GeoCenterZ
            )

            l = i.split('I')[1]
            l = l.split('J')[0]
            ncLine.GeoL = float(l)
            w = i.split('J')[1]
            w = w.split('Q')[0]
            ncLine.GeoW = float(w)
            le = i.split('Q')[1]
            le = re.split(r'[A-Z]', le)[0]
            ncLine.GeoMD = float(le)

            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Slot = True
            ncLine.Geo = True
            GEO = ncLine
            continue
        if "G65.1P9325" in i:
            last = len(path) - 1
            ncLine.GeoCenterX = path[last].X
            ncLine.GeoCenterY = path[last].Y
            ncLine.GeoCenterZ = path[last].Z
            ncLine.A = path[last].A
            ncLine.C = path[last].C

            Lx = path[last - 1].X
            Ly = path[last - 1].Y
            Lz = path[last - 1].Z

            ncLine.GeoVectorZ_X, ncLine.GeoVectorZ_Y, ncLine.GeoVectorZ_Z = Path.Path.Normalization(
                Lx - ncLine.GeoCenterX,
                Ly - ncLine.GeoCenterY,
                Lz - ncLine.GeoCenterZ
            )

            l = i.split('I')[1]
            l = l.split('J')[0]
            ncLine.GeoL = float(l)
            w = i.split('J')[1]
            w = w.split('K')[0]
            ncLine.GeoW = float(w)
            r = i.split('K')[1]
            r = r.split('Q')[0]
            ncLine.GeoR = float(r)
            le = i.split('Q')[1]
            le = re.split(r'[A-Z]', le)[0]
            ncLine.GeoMD = float(le)

            ncLine.GType = 1
            ncLine.BlockNum = block
            ncLine.Rect = True
            ncLine.Geo = True
            GEO = ncLine
            continue

        if "G65.1" in i or "M121" in i:
            block += 1
            has_BLOCK_END = True


        ncLine.ID = ID
        ID += 1
        path.append(ncLine)
    # =========================
    return path



def update_Nc_List(paths):
    new_text_lsit = []
    preblock = None
    for block in paths:
        if block.Line:
            text = block.OriginText
            # N00002G8.1X1076.053Y300.346Z450.000W-106.475U63.758F
            if block.IsSameAsPrePoint:
                text = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(preblock_withX.X), text)
                text = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(preblock_withX.Y), text)
                text = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(preblock_withX.Z), text)
                text = re.sub(r'W[-]*\d*.\d*', 'W{}'.format(preblock_withX.C), text)
                text = re.sub(r'U[-]*\d*.\d*', 'U{}'.format(preblock_withX.A), text)
            else:
                text = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(block.X), text)
                text = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(block.Y), text)
                text = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(block.Z), text)
                text = re.sub(r'U[-]*\d*.\d*', 'U{}'.format(block.A), text)
                text = re.sub(r'W[-]*\d*.\d*', 'W{}'.format(block.C), text)
            block.EditedText = text
            new_text_lsit.append(text)
        elif block.Cip:
            # N00493G8.5X1074.947Y180.792Z-101.298W-67.639U-37.791
            # N00494G8.5X1078.317Y180.449Z-102.990W-67.590U-38.080
            text1 = block.OriginTextIJK
            text2 = block.OriginTextXYZ
            text1 = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(block.I), text1)
            text1 = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(block.J), text1)
            text1 = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(block.K), text1)
            text1 = re.sub(r'U[-]*\d*.\d*', 'U{}'.format(round((block.A - preblock_withX.A) / 2 + block.A, 3)), text1)
            text1 = re.sub(r'W[-]*\d*.\d*', 'W{}'.format(round((block.C - preblock_withX.C) / 2 + block.C, 3)), text1)

            text2 = re.sub(r'X[-]*\d*.\d*', 'X{}'.format(block.X), text2)
            text2 = re.sub(r'Y[-]*\d*.\d*', 'Y{}'.format(block.Y), text2)
            text2 = re.sub(r'Z[-]*\d*.\d*', 'Z{}'.format(block.Z), text2)
            text2 = re.sub(r'U[-]*\d*.\d*', 'U{}'.format(block.A), text2)
            text2 = re.sub(r'W[-]*\d*.\d*', 'W{}'.format(block.C), text2)

            new_text_lsit.append(text1)
            new_text_lsit.append(text2)
        elif block.Geo:
            if block.Circ:  # N00505G65.1P9323I9.960Q2.00
                text = block.OriginText
                string1 = 'I{}Q{}'.format(block.GeoR * 2, block.GeoMD)
                text = re.sub(r'I\d*.\d*Q\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
                # 添加结束点坐标 (X1079.476Y115.046Z-105.255)
                vy = gp_Vec(block.GeoVectorY_X, block.GeoVectorY_Y, block.GeoVectorY_Z)
                vy.Normalize()
                vy = vy * block.GeoR
                x = vy.X() + block.GeoCenterX
                y = vy.Y() + block.GeoCenterY
                z = vy.Z() + block.GeoCenterZ
                t = '(X{}Y{}Z{})\n'.format(round(x, 3), round(y, 3), round(z, 3))
                new_text_lsit.append(t)
            elif block.Rect:  # N00006G65.1P9325I18.12J8.00K1.00Q2.00
                text = block.OriginText
                string1 = 'I{}J{}K{}Q{}'.format(block.GeoL, block.GeoW, block.GeoR, block.GeoMD)
                text = re.sub(r'I\d*.\d*J\d*.\d*K\d*.\d*Q\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
                # 添加vx点位    N00007G8.1X1099.712Y306.284Z-109.456W-106.475U63.758
                t = block.VX_TEXT
                vx = gp_Vec(block.GeoVectorX_X, block.GeoVectorX_Y, block.GeoVectorX_Z)
                vx.Normalize()
                vx = vx * block.GeoL / 2
                x = vx.X() + block.GeoCenterX
                y = vx.Y() + block.GeoCenterY
                z = vx.Z() + block.GeoCenterZ
                t1 = 'X{}Y{}Z{}'.format(round(x, 3), round(y, 3), round(z, 3))
                t = re.sub(r'X[-]*\d*.\d*Y[-]*\d*.\d*Z[-]*\d*.\d*', t1, t)
                new_text_lsit.append(t)
            elif block.Slot:  # N00014G65.1P9324I20.00J8.00Q0.00
                text = block.OriginText
                string1 = 'I{}J{}Q{}'.format(block.GeoL, block.GeoW, block.GeoMD)
                text = re.sub(r'I\d*.\d*J\d*.\d*Q\d*.\d*', string1, text)
                block.EditedText = text
                new_text_lsit.append(text)
                # 添加vx点位    N00007G8.1X1099.712Y306.284Z-109.456W-106.475U63.758
                t = block.VX_TEXT
                vx = gp_Vec(block.GeoVectorX_X, block.GeoVectorX_Y, block.GeoVectorX_Z)
                vx.Normalize()
                vx = vx * block.GeoL / 2
                x = vx.X() + block.GeoCenterX
                y = vx.Y() + block.GeoCenterY
                z = vx.Z() + block.GeoCenterZ
                t1 = 'X{}Y{}Z{}'.format(round(x, 3), round(y, 3), round(z, 3))
                t = re.sub(r'X[-]*\d*.\d*Y[-]*\d*.\d*Z[-]*\d*.\d*', t1, t)
                new_text_lsit.append(t)
            else:
                new_text_lsit.append(block.OriginText)
        else:
            new_text_lsit.append(block.OriginText)
        preblock = block
        if block.X is not None:
            preblock_withX = block
    return new_text_lsit


# 文件打开时，显示的后缀过滤器
NC_FILE_FORMAT = 'Mitsubishi NC File(*.nc)'
# 处理nc文件函数
READ_NC_FILE = read_Nc_File
# 更新NC文件
UPDATE_NC_LIST = update_Nc_List
# A轴旋转点Z值高度
A_CENTER_Z = -2
# 喷嘴高度
HEAD_HEIGHT = 2.0

A_AIX1 = gp_Ax1(gp_Origin(), gp_Dir(-1., 0., -1.))
C_AIX1 = gp_Ax1(gp_Origin(), gp_Dir(0., 0., -1.))
A_MODEL = './Preprocessor/vz10_a.brep'
C_MODEL = './Preprocessor/vz10_c.brep'