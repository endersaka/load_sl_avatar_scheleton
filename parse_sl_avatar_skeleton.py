import bpy
import mathutils
import xml.etree.ElementTree as ET

color_set_themes = [
    'DEFAULT', #'THEME01', # Theme 01 is terrible, so I commented it out
    'THEME02', 'THEME03', 'THEME04', 'THEME05', 'THEME06',
    'THEME07', 'THEME08', 'THEME09', 'THEME10', 'THEME11', 'THEME12', 'THEME13',
    'THEME14', 'THEME15', 'THEME16', 'THEME17', 'THEME18', 'THEME19', 'THEME20'
]
current_color_set = 1
pose_bones_groups_map = []
pose_bones_group_names = []

tree = ET.parse('D:\\Program Files\\SecondLifeViewer\\character\\avatar_skeleton.xml')
root = tree.getroot()

armature_obj = bpy.context.scene.objects.get('avatar_skeleton')
print('avatar skeleton object: ' + str(armature_obj))

# Conveniece function to convert XML attributes representing a three coordinates vector
# like `pos="0.000 0.000 0.084"` to a Python list.
def pos_str_to_list(pos_str):
    return [float(coord) for coord in pos_str.split()]

# Python builtin function `bool()` isn't able to parse lowercase 'false' or 'true'.
# Therefore we need a custom function to parse `connected` attribute value.
#
# Neither `eval()` or `ast.literal_eval()` (suggested by some developers) can parse
# lowercase 'true' or 'false' to `True` or `False`, the former throws a `NameError`
# instead (ex: "NameError: name 'false' is not defined") and the later a `ValueError`
# (ex: "ValueError: malformed node or string on line 1: <ast.Name object at 0x000001F78BADFA30>")
def to_bool(str):
    result = False
    if str == 'false':
        result = False
    elif str == 'true':
        result = True
    return result

def read_children(el):
    global pose_bones_groups_map, color_set_themes, current_color_set, pose_bones_group_names
    children = el.findall('*')
    for child in children:
        #if child.tag == 'bone':
        # print(child.tag + ': ' + str(child.attrib))
        
        # Set default parent
        parent_edit_bone = None
        
        # Get parent if any...
        if el != None and el.tag != 'linden_skeleton':
            parent_edit_bone = armature_obj.data.edit_bones.get(el.attrib['name'])
        
        # Create a bone.
        edit_bone = armature_obj.data.edit_bones.new(child.attrib['name'])
        
        # Set default parent position vector to origin.
        parent_pos_vec = mathutils.Vector((0.0, 0.0, 0.0))
        
        # Get parent head position vector.
        if parent_edit_bone != None:
            # Get parent bone position
            parent_pos_vec = mathutils.Vector(parent_edit_bone.head)
        
        # Convert current bone `pos` and `end` attributes to `mathutils.Vector`
        pos_vec = mathutils.Vector(pos_str_to_list(child.attrib['pos']))
        end_vec = mathutils.Vector(pos_str_to_list(child.attrib['end']))
        
        head_vec = parent_pos_vec + pos_vec
        tail_vec = head_vec + end_vec
        
        # Set bone head and tail position.
        edit_bone.head = head_vec.to_tuple()
        edit_bone.tail = tail_vec.to_tuple()
        
        # Set parent and connected properties
        if parent_edit_bone != None:
            # Set parent bone
            edit_bone.parent = parent_edit_bone
            
            if 'connected' in child.attrib:
                # Set bone connected
                edit_bone.use_connect = to_bool(child.attrib['connected'])
        
        # @note Unespectedly, while bone groups can be created in Edit Mode to assign
        # a group to the current edit bone we need to toggle to Pose Mode, therefore
        # I placed group assignment in an external function to avoid frequent switch
        # to and from Pose Mode.
        #
        # Try to get the bone group (or create it, if not present).
        group = None
        group_name = child.attrib['group']
        print('Attempt to assign group "' + group_name + '" to bone "' + edit_bone.name + '"...')
        
        if group_name in armature_obj.pose.bone_groups.keys():
            print('Get the group...')
            group = armature_obj.pose.bone_groups.get(group_name)
        else:
            print('Group "' + group_name + '" doesn\'t exist: create a new one...')
            # Create a bones group if not created yet
            group = armature_obj.pose.bone_groups.new(name=child.attrib['group'])
            
            # Assign the group a color set.
            group.color_set = color_set_themes[current_color_set]
            
            current_color_set = current_color_set + 1
            if current_color_set >= len(color_set_themes):
                current_color_set = 0
                    
        pose_bones_groups_map.append([edit_bone.name, group_name])
        
        pose_bones_group_names.append(group_name)
        bone_layer_index = pose_bones_group_names.index(group_name) + 1
        if bone_layer_index < 32:
            edit_bone.layers[bone_layer_index] = True
        
        #print('Got group "' + group.name + '", assign it to bone "' + edit_bone.name + '"...')
        #
        # Assign the group to the bone
        #print('Get the pose bone named "' + edit_bone.name + '"...')
        #pose_bone = armature_obj.pose.bones.get(edit_bone.name)
        #if pose_bone != None:
        #    print('Assign the group "' + group.name + '" to pose bone "' + pose_bone.name + '"...')
        #    pose_bone.bone_group = group
        
        # Collision volumes seems to be leaf nodes.
        if child.tag == 'bone':
            read_children(child)
#        elif child.tag == 'collision_volume':
#            print(child.tag + ': ' + str(child.attrib))


def assign_bone_groups():
    global pose_bones_groups_map, armature_obj
    bpy.ops.object.posemode_toggle()
    for pair in pose_bones_groups_map:
        bone_group = armature_obj.pose.bone_groups.get(pair[1])
        if bone_group != None and isinstance(bone_group, bpy.types.BoneGroup):
            armature_obj.pose.bones.get(pair[0]).bone_group = bone_group


if armature_obj == None:
    armature_data = bpy.data.armatures.get('avatar_skeleton_data')
    if armature_data == None:
        armature_data = bpy.data.armatures.new('avatar_skeleton_data')
    
    armature_obj = bpy.data.objects.new('avatar_skeleton', armature_data)
    bpy.context.scene.collection.objects.link(armature_obj)

if armature_obj != None and armature_obj.type == 'ARMATURE':
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    
    armature_obj.select_set(True)
    
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')

    read_children(root)
    assign_bone_groups()
