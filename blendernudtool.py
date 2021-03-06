"""
Credit:
    Original scripts:
        @RandomTBush
        @Soneek
        @Mariosonicds
        @Smb123w64gb
    Blender Script (twitter):
        @Astril_Knight
        @Smb123w64gb
"""

import bmesh
from BitUtil import *
import os
#from mathutils import Vector
import bpy
import shutil


class Bone_Info_Struct:
        structType = "bone"
        def __init__(self,Bone1,Bone2,Bone3,Bone4):
            self.Bone1 = Bone1
            self.Bone2 = Bone2
            self.Bone3 = Bone3
            self.Bone4 = Bone4
        
        
class Weight_Info_Struct:
    structType = "weightData"
    def __init__(self,Weight1,Weight2,Weight3,Weight4):
        self.Weight1 = Weight1
        self.Weight2 = Weight2
        self.Weight3 = Weight3
        self.Weight4 = Weight4
    
class weight_data_struct:
    def __init__(self,boneids,weights):
        self.boneids = boneids
        self.weights = weights

def readModel():
    clearConsole()
    cwd = os.getcwd()
    realpath = os.path.join(cwd, bpy.context.scene.SSB4UMT.path)
    nud = open(realpath + '\\model.nud', 'rb')
    if bpy.context.scene.SSB4UMT.vbnEnable == True:
        vbn = open(realpath + '\\model.vbn', 'rb')
    else:
        vbn = None
    bpy.context.scene.SSB4UMT.name_positioner = '[]'
    # nut = open('model.nut','rb')
    colormult = bpy.context.scene.SSB4UMT.colormult


    BoneCount = []
    BoneName_Array = []
    BoneParent_Array = []
    Bone_Matrix_Array = []
    BoneArray = []
    VertexStart_array = []
    VertexAmount_array = []
    VertexSize_array = []
    PolyStart_array = []
    PolyAmount_array = []
    PolySize_array = []
    VertexAddStart_array = []
    UVSize_array = []
    PolyName_array = []
    Color_Array = []
    Alpha_Array = []
    SingleBind_array = []
    TexturePropertiesL1Start_array = []
    TexturePropertiesL2Start_array = []
    TexturePropertiesL3Start_array = []
    TexturePropertiesL4Start_array = []
    TextureNumL1_array = []
    TextureNumL2_array = []
    TextureNumL3_array = []
    TextureNumL4_array = []
    Trans_array = []
    Rotation_array = []
    Scale_array = []

    # read archive strings, pointers, and floats
    NDP3 = readu32be(nud)
    # Checks if NDP3 file
    if NDP3 != 1313099827:
        raise ValueError("Not a valid NDP3 file")
    else:
        print("NDP3 Verified")
        
    fileSize = readu32be(nud)
    unknownlong1 = readu16be(nud)
    polysets = readu16be(nud)
    unknownlong2 = readu32be(nud)
    PolyClumpStart = readu32be(nud) + 48
    PolyClumpSize = readu32be(nud)
    VertexClumpStart = PolyClumpStart + PolyClumpSize
    VertexClumpSize = readu32be(nud)
    VertexAddClumpStart = VertexClumpStart + VertexClumpSize
    VertexAddClumpSize = readu32be(nud)
    NameClumpStart = VertexAddClumpStart + VertexAddClumpSize
    unknownFloat1 = readfloatbe(nud)
    unknownFloat2 = readfloatbe(nud)
    unknownFloat3 = readfloatbe(nud)
    unknownFloat4 = readfloatbe(nud)
    # Model Extraction from NUD file
    ObjCount = 0
    for polyid in range(polysets):  # polysets
        floata = readu32be(nud)
        floatb = readu32be(nud)
        floatc = readu32be(nud)
        floatd = readu32be(nud)
        floate = readu32be(nud)
        floatf = readu32be(nud)
        floatg = readu32be(nud)
        floath = readu32be(nud)
        polynamestart = readu32be(nud)
        identifiera = readu32be(nud)
        singlebind = readu16be(nud) + 1
        if singlebind == 65536:
            singlebind = 1
        polyamount = readu16be(nud)
        positionb = readu32be(nud)
        ObjCount += polyamount
        for polyid in range(polyamount):
            PolyName_array.append(polynamestart)
            SingleBind_array.append(singlebind)

    for objid in range(ObjCount):
        PolyStart = readu32be(nud) + PolyClumpStart
        VertexStart = readu32be(nud) + VertexClumpStart
        VertexAddStart = readu32be(nud) + VertexAddClumpStart
        VertexAmount = readu16be(nud)
        VertexSize = readByte(nud)
        UVSize = readByte(nud)
        TextureLayer1Properties = readu32be(nud)
        TextureLayer2Properties = readu32be(nud)
        TextureLayer3Properties = readu32be(nud)
        TextureLayer4Properties = readu32be(nud)
        PolyAmount = readu16be(nud)
        PolySize = readByte(nud)
        PolyFlag = readByte(nud)
        nud.read(0x0C)
        # Append values
        VertexStart_array.append(VertexStart)
        PolyStart_array.append(PolyStart)
        VertexAddStart_array.append(VertexAddStart)
        VertexAmount_array.append(VertexAmount)
        PolyAmount_array.append(PolyAmount)
        VertexSize_array.append(VertexSize)
        UVSize_array.append(UVSize)
        PolySize_array.append(PolySize)
        TexturePropertiesL1Start_array.append(TextureLayer1Properties)
        TexturePropertiesL2Start_array.append(TextureLayer2Properties)
        TexturePropertiesL3Start_array.append(TextureLayer3Properties)
        TexturePropertiesL4Start_array.append(TextureLayer4Properties)
    """
    #VBN Read
    BoneCount = 0
    if vbn:
        VBN = readu32le(vbn)
        vbn.seek(8)
        if VBN == 1447185952:
            #little Endian
            print("VBN Verified\n")
            BoneCount = readu32le(vbn)
            vbn.seek(int("1C",16))
            for x in range(BoneCount):
                jumpman = vbn.tell() + int("44",16)
                BoneName = readString(vbn)
                if x < 10:
                    BoneName = "00" + str(x+1) + ' - ' + BoneName
                elif 100 > x > 9:
                    BoneName = "0" + str(x+1) + ' - ' + BoneName
                elif x > 99:
                    BoneName = str(x+1) + BoneName
                vbn.seek(jumpman)
                BoneParent = readu16le(vbn) + 1
                vbn.read(2)
                if BoneParent == 0:
                    BoneParent = -1
                vbn.read(4)
                BoneName_Array.append(BoneName)
                BoneParent_Array.append(BoneParent)
            Trans_array = []
            Rotation__array = []
            Scale_array = []
            BoneArray = []
            for x in range(BoneCount):
                #Transform
                tx = readfloatle(vbn)
                ty = readfloatle(vbn)
                tz = readfloatle(vbn)
                #Rotation
                rx = readfloatle(vbn)
                ry = readfloatle(vbn)
                rz = readfloatle(vbn)
                #Size
                sx = readfloatle(vbn)
                sy = readfloatle(vbn)
                sz = readfloatle(vbn)
                #Name & Parent
                BoneName = BoneName_Array[x]
                BoneParent = BoneParent_Array[x]
                #Append coord to array
                Trans_array.append([tx,ty,tz])
                Rotation_array.append([rx,ry,rz])
                Scale_array.append([sx,sy,sz])

        elif VBN == 541999702:
            #Big Endian
            print("VBN Verified")
            BoneCount = readu32be(vbn)
        else:
            raise ValueError("Not a valid VBN file")
    else:
        print("VBN feature disabled")
    """
    for z in range(ObjCount):
        Face_array = []
        Vert_array = []
        Color_array = []
        Alpha_array = []
        Normal_array = []
        UV_array = []
        UV2_array = []
        UV3_array = []
        UV4_array = []
        B1_array = []
        W1_array = []
        Weight_array = []
        nud.seek(VertexStart_array[z])
        for x in range(VertexAmount_array[z]):
                if VertexSize_array[z] != 0x08 and VertexSize_array[z] >= 0x40:
                        vx = readfloatbe(nud)
                        vy = readfloatbe(nud)
                        vz = readfloatbe(nud)
                elif VertexSize_array[z] == 0x08:
                        vx = 0
                        vy = 0
                        vz = 0
                if VertexSize_array[z] == 0x00:
                        unknownfloat = readfloatbe(nud)
                if VertexSize_array[z] >= 0x06:
                        nx = readhalffloatbe(nud)
                        ny = readhalffloatbe(nud)
                        nz = readhalffloatbe(nud)
                        nq = readhalffloatbe(nud)
                        if VertexSize_array[z] == 0x07:
                                nud.seek(0x10, 1)
                        elif VertexSize_array[z] == 0x08:
                                nud.seek(0xA, 1)
                        if UVSize_array[z] == 0x10:
                                tu = readhalffloatbe(nud) * 2
                                tv = ((readhalffloatbe(nud) * 2) * -1) + 1
                        if UVSize_array[z] >= 0x12:
                                colorr = readByte(nud)
                                colorg = readByte(nud)
                                colorb = readByte(nud)
                                colora = readByte(nud) / 127
                                tu = readhalffloatbe(nud) * 2
                                tv = ((readhalffloatbe(nud) * 2) * -1) + 1
                        if UVSize_array[z] >= 0x22:
                            tu2 = readhalffloatbe(nud) * 2
                            tv2 = ((readhalffloatbe(nud) * 2) * -1) + 1
                            UV2_array.append([tu2,tv2,0])
                        if UVSize_array[z] >= 0x32:
                            tu3 = readhalffloatbe(nud) * 2
                            tv3 = ((readhalffloatbe(nud) * 2) * -1) + 1
                            UV2_array.append([tu3,tv3,0])
                        if UVSize_array[z] >= 0x42:
                            tu4 = readhalffloatbe(nud) * 2
                            tv4 = ((readhalffloatbe(nud) * 2) * -1) + 1
                            UV2_array.append([tu4,tv4,0])
                        Bone1 = SingleBind_array[z]
                        Bone2 = 0
                        Bone3 = 0
                        Bone4 = 0
                        Weight1 = 0
                        Weight2 = 0
                        Weight3 = 0
                        Weight4 = 0
                        Color_array.append([colorr, colorg, colorb])
                        Alpha_array.append(colora)
                        UV_array.append([tu, tv, 0])
                        if VertexSize_array[z] < 0x40:
                                Vert_array.append([vx, vy, vz])
                                Normal_array.append([nx, ny, nz])
                                B1_array.append(Bone_Info_Struct(Bone1,
                                                                 Bone2,
                                                                 Bone3,
                                                                 Bone4))
                                W1_array.append(Weight_Info_Struct(Weight1,
                                                                   Weight2,
                                                                   Weight3,
                                                                   Weight4))
        if VertexSize_array[z] >= 0x40:
                nud.seek(VertexAddStart_array[z])
                for x in range(VertexAmount_array[z]):
                        vx = readfloatbe(nud)
                        vy = readfloatbe(nud)
                        vz = readfloatbe(nud)
                        if VertexSize_array[z] == 0x40:
                                unknownfloat = readfloatbe(nud)
                        if VertexSize_array[z] >= 0x46:
                                nx = readhalffloatbe(nud)
                                ny = readhalffloatbe(nud)
                                nz = readhalffloatbe(nud)
                                nq = readhalffloatbe(nud)
                                if VertexSize_array[z] == 0x47:
                                        nud.seek(0x10,1)
                        Bone1 = readByte(nud) + 1
                        Bone2 = readByte(nud) + 1
                        Bone3 = readByte(nud) + 1
                        Bone4 = readByte(nud) + 1
                        Weight1 = readByte(nud) / 255
                        Weight2 = readByte(nud) / 255
                        Weight3 = readByte(nud) / 255
                        Weight4 = readByte(nud) / 255
                        Vert_array.append([vx, vy, vz])
                        Normal_array.append([nx, ny, nz])
                        B1_array.append(Bone_Info_Struct(Bone1,
                                                         Bone2,
                                                         Bone3,
                                                         Bone4))
                        W1_array.append(Weight_Info_Struct(Weight1,
                                                           Weight2,
                                                           Weight3,
                                                           Weight4))


        vert_length = len(Vert_array)
        nud.seek(PolyStart_array[z])
        if PolySize_array[z] == 0x00:
            FaceCount = PolyAmount_array[z]
            FaceStart = nud.tell()
            VerStart = (FaceCount * 2) + FaceStart
            StartDirection = 1
            f1 = readu16be(nud) + 1
            f2 = readu16be(nud) + 1
            FaceDirection = StartDirection
            while nud.tell() != VerStart:
                dotell = nud.tell()
                f3 = readu16be(nud)
                if f3 == 0xFFFF:
                    f1 = readu16be(nud) + 1
                    f2 = readu16be(nud) + 1
                    FaceDirection = StartDirection
                else:
                    f3 += 1
                    FaceDirection *= -1
                    if f1 != f2 and f2 != f3 and f3 != f1:
                        if FaceDirection > 0:
                            Face_array.append([f3 - 1, f2 - 1, f1 - 1])
                        else:
                            Face_array.append([f2 - 1, f3 - 1, f1 - 1])
                    f1 = f2
                    f2 = f3
        elif PolySize_array[z] == 0x40:
            for x in range(0, (PolyAmount_array[z] // 3)):
                fa = readu16be(nud)
                fb = readu16be(nud)
                fc = readu16be(nud)
                Face_array.append([fa, fb, fc])
                
        #Add import data to scene
        nud.seek(NameClumpStart + PolyName_array[z])
        name = readString(nud)
        mymesh = bpy.data.meshes.new(name)
        myobject = bpy.data.objects.new(name, mymesh)
        myobject.location = bpy.context.scene.cursor_location
        bpy.context.scene.objects.link(myobject)
        mymesh.from_pydata(Vert_array, [], Face_array)
        mymesh.update(calc_edges=True)
        
        
    tmp_name = []
    
    
    for obj in bpy.context.scene.objects:
        tmp_name.append(obj.name)
    
    bpy.context.scene.SSB4UMT.name_positioner = str(tmp_name)
    
    bpy.ops.object.select_all()
    bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all()
    print("import successful!")

# Inject code

def injectModel():
    class poly(object):

        def __init__(self, name, id):
            self.name = name
            self.id = id
            self.vertexCoords = []

    clearConsole()
    shutil.copy2(bpy.context.scene.SSB4UMT.path +
                 'model.nud', bpy.context.scene.SSB4UMT.out)
    print("Nud reference created")


    polyNames = []
    replacePolys = []
    
    # Reverse objects order to original
    for i in reversed(eval(bpy.context.scene.SSB4UMT.name_positioner)):
        polyNames.append(i)
    # Create poly structure for inject
    for polyName, polynum in zip(polyNames, range(len(polyNames))):
        replacePolys.append(poly(polyName, polynum))
        for vert in bpy.context.scene.objects[polyName].data.vertices:
            tmpref = list(vert.co)
            for x in range(3):
                tmpref[x] = str(round(tmpref[x], 5))
                if x != 0:
                    tmpref[x] = ' ' + tmpref[x]
            tmpref.append(' ')
            replacePolys[polynum].vertexCoords.append(tmpref)

    f = open(bpy.context.scene.SSB4UMT.out + 'model.nud', 'rb+')
    polys = []
    verts = []
    f.seek(0x0A, 1)
    polyset_count = readu16be(f)
    f.seek(0x04, 1)
    face_clump_start = readu32be(f) + 0x30
    face_clump_size = readu32be(f)
    vert_clump_start = (face_clump_start + face_clump_size)
    vert_clump_size = readu32be(f)
    vert_add_clump_start = (vert_clump_start + vert_clump_size)
    vert_add_clump_size = readu32be(f)
    name_clump_start = (vert_add_clump_start + vert_add_clump_size)
    f.seek(0x10, 1)
    bodygroups = {}
    for i in range(polyset_count):
        for j in range(8):
            f.seek(4, 1)
        f.tell()
        name_start = readu32be(f)
        identifiera = readu32be(f)
        singlebind = readu16be(f)
        if singlebind == 0xFFFF:
            singlebind = 1
        else:
            singlebind += 1
        poly_count = readu16be(f)
        positionb = readu32be(f)
        for j in range(poly_count):
            polys.append({'name': name_start,
                          'identifiera': identifiera,
                          'positionb': positionb,
                          'singlebind': singlebind,
                          'pgroup': i
                          })
    for i, poly in enumerate(polys):
        print(polyNames[i])
        next_poly_addr = f.tell() + 0x30
        face_start = readu32be(f) + face_clump_start
        vert_start = readu32be(f) + vert_clump_start
        vert_add_start = readu32be(f) + vert_add_clump_start
        vert_count = readu16be(f)
        vert_size = readByte(f)
        uv_size = readByte(f)
        tex1_props = readu32be(f)
        tex2_props = readu32be(f)
        tex3_props = readu32be(f)
        tex4_props = readu32be(f)
        face_count = readu16be(f)
        face_size = readByte(f)
        face_flags = readByte(f)
        vert_len = int(len(verts) / 3)
        f.seek(poly['positionb'])
        mystery = f.read(0x60)
        #mystery = binascii.hexlify(mystery)
        f.seek(poly['positionb'] + 0x3c)
        bodygroup_id = readu32be(f)
        bodygroups[bodygroup_id] = poly['pgroup']
        f.seek(name_clump_start + poly['name'])
        poly_name = readString(f)
        f.seek(vert_start)
        for j in range(vert_count):
            if vert_size == 0x08 or vert_size >= 0x40:
                vx = 0
                vy = 0
                vz = 0
            if not vert_size >= 0x40:
                for v in range(3):
                    f.write(
                        struct.pack(
                            ">f", float(
                                replacePolys[i].vertexCoords[j][v])))
            if vert_size == 0x00:
                f.seek(0x04, 1)
            elif vert_size == 0x06:
                f.seek(0x08, 1)
            elif vert_size == 0x07:
                f.seek(0x18, 1)
            elif vert_size == 0x08:
                f.seek(0x11, 1)
            if vert_size == 0x00 or \
                    (uv_size == 0x12 or uv_size == 0x22 or uv_size == 0x42):
                f.seek(0x04, 1)
            if uv_size >= 0x12 or vert_size == 0x06:
                f.seek(0x04, 1)
                if uv_size >= 0x22:
                    f.seek(0x04, 1)
                if uv_size >= 0x32:
                    f.seek(0x04, 1)
                if uv_size >= 0x42:
                    f.seek(0x04, 1)
        if vert_size >= 0x40:
            f.seek(vert_add_start)
            for j in range(vert_count):
                for v in range(3):
                    f.write(
                        struct.pack(
                            ">f", float(
                                replacePolys[i].vertexCoords[j][v])))
                if vert_size == 0x40:
                    f.seek(0x04, 1)
                f.seek(0x08, 1)
                if vert_size == 0x46:
                    f.seek(0x08, 1)
                elif vert_size == 0x47:
                    f.seek(0x18, 1)
        f.seek(next_poly_addr)
    f.close()
    print("Injection Complete!")
