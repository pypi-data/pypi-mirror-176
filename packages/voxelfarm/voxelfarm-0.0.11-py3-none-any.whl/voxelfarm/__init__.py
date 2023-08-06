voxelfarm_framework = None

class type:
    view = 1 << 1
    project = 1 << 2
    voxel_terrain = 1 << 3
    voxel_operations = 1 << 4
    block_model = 1 << 5
    point_cloud = 1 << 6
    voxel_generator = 1 << 7
    point_cloud_raw = 1 << 8
    heightmap_raw = 1 << 9
    block_model_raw = 1 << 10
    mesh_raw = 1 << 11
    mesh = 1 << 12
    ortho = 1 << 13
    program = 1 << 14
    folder = 1 << 15
    raw_density = 1 << 16
    indexed_density = 1 << 17
    material_tracking = 1 << 18
    voxel_mesh = 1 << 19
    drill_holes = 1 << 20
    drill_holes_raw = 1 << 21
    indexed_ortho = 1 << 22
    voxel_points = 1 << 23
    voxel_plane = 1 << 24
    wms_ortho = 1 << 25
    voxel_ortho = 1 << 26
    export = 1 << 27
    report = 1 << 28
    raw_geo_chem = 1 << 29
    geo_chem = 1 << 30
    value = 1
    set = 2

class attribute:
    none = 0
    volume = 1
    material = 1 << 1
    color = 1 << 2
    vector = 1 << 3
    normal = 1 << 4
    tangent = 1 << 5
    uv = 1 << 6
    color_difference = 1 << 7
    voxel_index = 1 << 8
    faces = 1 << 9
    merge = 1 << 10 
    disable_compression = 1 << 11
    fix_self_intersections = 1 << 12

class attribute_merge_mode:
    none = 0
    add = 1
    multiply = 2
    min = 3
    max = 4
    average = 5
    unit = 6
    grade = 7

class layer_merge_mode:
    none = 0
    min = 1
    max = 2
    override = 3

class texture:
    diffuse = 0
    normal = 1
    rgb0 = 2
    rgb1 = 3
    rgb2 = 4
    rgba0 = 1
    rgba1 = 1
    rgba2 = 1

class ColorLegend:
    gradient_step = 1.0
    gradient_min = 0.0
    gradient_max = 100.0
    gradient_attribute = ""
    static_color = (0, 0, 0)

class DrillHoleOptions:
    show_collars = True
    show_cylinders = True

class Material:
    color = (1.0, 1.0, 1.0, 1.0)
    gradient = None
    diffuse = False
    normal = False
    gradient = ""
    def serialize(self):
        result = "0,"
        result += str(self.color[0]) + ","
        result += str(self.color[1]) + ","
        result += str(self.color[2]) + ","
        result += str(self.color[3]) + ","
        result += ("1" if self.diffuse else "0") + ","
        result += ("1" if self.normal else "0") + ","
        result += self.gradient
        return result

def init():
    pass

def set_vector(index, vx, vy, vz):
    pass

def set_material(index, id):
    pass

def set_field(index, field):
    pass

def get_voxel_origin(index):
    return (0,0,0)

def get_field_origin(index):
    return (0,0,0)

def get_field_origin_x(index):
    return 0.0

def get_field_origin_y(index):
    return 0.0

def get_field_origin_z(index):
    return 0.0

def input(id, label, default = 0.0):
    return voxelfarm_framework.input(id, label, default)

def set_entity_bounds_x(v0, v1):
    pass

def set_entity_bounds_y(v0, v1):
    pass

def set_entity_bounds_z(v0, v1):
    pass

def cellIsEmpty():
    pass

def test():
    pass


