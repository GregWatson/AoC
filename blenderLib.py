import bpy


def run_ops_without_view_layer_update(func, arg):
    from bpy.ops import _BPyOpsSubModOp

    view_layer_update = _BPyOpsSubModOp._view_layer_update

    def dummy_view_layer_update(context):
        pass

    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update

        func(arg)

    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update


def addCuboid(POS=(0,0,0), SCALE=(1,1,1),COL=(1,0,0,1)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.5*SCALE[0],0.5*SCALE[1],0.5*SCALE[2]))
    obj = bpy.context.object #stores the active object (the cube created above)
    bpy.ops.transform.resize( value=SCALE ) #resizes the cube
    bpy.ops.object.transform_apply( scale=True ) #don't forget to apply!!
    if obj.data.materials:
        material = obj.data.materials[0]
    else:
        material = bpy.data.materials.new(name="Material")
        obj.data.materials.append(material)

    # Set the color
    material.diffuse_color = COL

    obj.location.x += POS[0]
    obj.location.y += POS[1]
    obj.location.z += POS[2]

def addVertCylinder(POS=(0,0,0), SCALE=(1,1,1),COL=(1,0,0,1)):
    bpy.ops.mesh.primitive_cylinder_add( vertices=32, radius=0.5, depth=1.0, end_fill_type='NGON', calc_uvs=True, 
                                        enter_editmode=False, align='WORLD', 
                                        location=(0.5*SCALE[0],0.5*SCALE[1],0.5*SCALE[2]), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)
                                        )
    
    obj = bpy.context.object #stores the active object (the cube created above)
    bpy.ops.transform.resize( value=SCALE ) #resizes the cube
    bpy.ops.object.transform_apply( scale=True ) #don't forget to apply!!

    if obj.data.materials:
        material = obj.data.materials[0]
    else:
        material = bpy.data.materials.new(name="Material")
        obj.data.materials.append(material)

    # Set the color
    material.diffuse_color = COL

    obj.location.x += POS[0]
    obj.location.y += POS[1]
    obj.location.z += POS[2] 


GREY80= (0.8, 0.8, 0.8, 1)
GREEN80= (0, 0.8, 0, 1)
RED=(1,0,0,1)
RED80 = (0.8,0,0,1)
WHITE=(1,1,1,1)


# map a 7 bit char to a color
def charToCol(c):
    i = ord(c)
    r = i >> 5
    g = (i >> 2) & 3
    b = i & 3
    return (r,g,b,1)