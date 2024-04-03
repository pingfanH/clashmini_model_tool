import bpy
import json
from clashmini_model_expoter.utils.glb import GlbParser
from clashmini_model_expoter.utils.glb import GlbEncoder
import os;
import asyncio
bl_info = {
    "name": "Clash-mini-Exporter",
    "description": "",
    "author": "Pingfanh",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "3D View"
}


class ModelExport(bpy.types.Operator):
    bl_idname = "item.model_export"
    bl_label = "Export Model"
    #bl_description = "Rename all mesh UV maps to the same, by this u can join meshes into one without losing UV"
    #id: bpy.props.IntProperty(name="id", default=0) # type: ignore
    def execute(self, context):
        obj = bpy.context.object
        output_path = obj.model_path
        bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLTF_SEPARATE',  # 导出模型和纹理为单独文件
        use_selection=True,  # 仅导出选中的对象
        #export_apply=True  # 应用所有变换
        )
        json_model = json.load(open(output_path))
        clash_mini_model(json_model)
        #print(json_model)
        with open(output_path, 'w') as json_file:
            json.dump(json_model, json_file, indent=4)

        gltf2glb(output_path)

        with open(output_path.replace(".gltf",".glb"), 'rb') as src:
            with open(os.path.dirname(output_path)+"/"+os.path.basename(output_path).replace(".gltf","")+"_lod1.glb", 'wb') as dest:
                dest.write(src.read())
        with open(output_path.replace(".gltf",".glb"), 'rb') as src:
            with open(os.path.dirname(output_path)+"/"+os.path.basename(output_path).replace(".gltf","")+"_lod2.glb", 'wb') as dest:
                dest.write(src.read())
        
        os.remove(output_path)
        os.remove(output_path.replace(".gltf",".bin"))
        return {'FINISHED'}

class ExporterPanel(bpy.types.Panel):
    bl_label = bl_info["name"]
    bl_idname = "Exporter_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = bl_info["name"]

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text=bl_info["name"]+" version-0.0.1", icon='WORLD_DATA')
        
        row = layout.row()
        row.label(text="ModelPath:")
        
        row = layout.row()
        row.prop(obj, "model_path", text="")
        
        row = layout.row()
        row.operator("item.model_export",text="导出", icon='MESH_CUBE')

# 注册自定义节点
def register():
    bpy.utils.register_class(ExporterPanel)
    bpy.utils.register_class(ModelExport)
    bpy.types.Object.model_path = bpy.props.StringProperty(
        name="Model Path",
        default="",
        update=update_text
        )

# 注销自定义节点
def unregister():
    bpy.utils.unregister_class(ExporterPanel)
    bpy.utils.unregister_class(ModelExport)
    del bpy.types.Object.model_path

def update_text(self, context):
    # Save the text value to a persistent location
    # For example, you could use Blender's user preferences
    bpy.context.user_preferences.addons[__name__].preferences.model_path = self.model_path

def load_text():
    # Load the text value from a persistent location
    # For example, you could use Blender's user preferences
    return bpy.context.user_preferences.addons[__name__].preferences.model_path

def clash_mini_model(json_model):
    json_model["materials"]=[]
    json_model["textures"]=[]
    json_model["images"]=[]
    json_model["asset"]={
    "version": "2.0"
    }
    json_model["extensionsUsed"]=[
        "KHR_materials_unlit",
        "SC_shader"
    ]
    
    material_convert(json_model)

def material_convert(json_model):
    # 获取当前选择的对象
    objs = bpy.context.selected_objects
    for obj in objs:
        # 确保对象存在并且是网格对象
        if obj and obj.type != 'MESH':
            continue

        # 遍历对象的所有材质槽
        for slot in obj.material_slots:
            material = slot.material
            if material is None and material.node_tree is None:
                continue
            temp_material = {
                "extensions": {
                    "KHR_materials_unlit": {},
                    "SC_shader": {
                        "blendMode": 4,
                        "constants": [
                            "AMBIENT",
                            "DIFFUSE",
                            "SHADOWMAP",
                            "OPACITY"
                        ],
                        "name": "barbarianking",
                        "shader": "uber_pbr",
                        "variables": {
                            "IOR": 1.4500000476837158,
                            "Tangent": [
                                0,
                                0,
                                0
                            ],
                            "ambient": [
                                1,
                                1,
                                1,
                                1
                            ],
                            "ambientIntensity": 0.20000000298023224,
                            "diffuseTex2D": {
                                "index": 1
                            },
                            "directRadianceStrength": 1,
                            "emission": [
                                1,
                                1,
                                1,
                                1
                            ],
                            "emissionStrength": 0,
                            "enableEmissionTex": False,
                            "enableFresnel": True,
                            "enableGammaCorrection": False,
                            "enableHDR": True,
                            "enableMRA": True,
                            "enableMainUVAnim": False,
                            "enableReflection": True,
                            "enableResetScale": False,
                            "enableSSS": True,
                            "enableSceneFlag": False,
                            "enableStencil": False,
                            "enableUVAnim": False,
                            "enableUVAnimMultiply": False,
                            "fresnelColor": [
                                0.5,
                                0.5,
                                0.5,
                                1
                            ],
                            "fresnelMask": 0,
                            "fresnelStrength": 1,
                            "lightColor": [
                                1,
                                1,
                                1,
                                1
                            ],
                            "lightDir": [
                                0,
                                1,
                                -1
                            ],
                            "lightFlowMaskTex2D": "",
                            "lightFlowTex2D": "",
                            "metalness": 0.5,
                            "mraTex2D": {
                                "index": 2
                            },
                            "normal": [
                                0.5,
                                0.5,
                                1
                            ],
                            "opacity": [
                                1,
                                1,
                                1,
                                1
                            ],
                            "reflectioinTex2D": {
                                "index": 3
                            },
                            "roughness": 0.5,
                            "specularStrength": 1,
                            "sssMaskTex2D": {
                                "index": 4
                            },
                            "sssStrength": 1,
                            "sssTex2D": {
                                "index": 5
                            },
                            "stencilOffset": [
                                0,
                                0,
                                0
                            ],
                            "stencilScale": [
                                0,
                                0,
                                0
                            ],
                            "stencilTex2D": "",
                            "teamColor": [
                                1,
                                1,
                                1,
                                1
                            ],
                            "teamColorTex2D": {
                                "index": 6
                            },
                            "textureUV": [
                                0,
                                0,
                                0
                            ],
                            "textureUV2": [
                                0,
                                0,
                                0
                            ],
                            "u_convertTosRGB_maya": False,
                            "u_convertsrgb_maya": True,
                            "uvSpeedAnim": [
                                0,
                                0,
                                0
                            ]
                        }
                    }
                }
            }
            SC_shader = temp_material["extensions"]["SC_shader"]
            SC_shader["name"] = material.name
            SC_shader_var=SC_shader["variables"]
            print("Material Name:", material.name)
            # 遍历节点树中的所有节点
            for node in material.node_tree.nodes:
                if node.type != 'GROUP':
                    continue
                print("Group Name:", node.node_tree.name)
                # 获取群组中的参数
                for input_socket in node.inputs:

                    if input_socket.is_linked:
                        # 获取连接到输入插座的值
                        linked_node = input_socket.links[0].from_node
                        if linked_node.type == 'TEX_IMAGE':
                            # 获取图像纹理节点的图像路径
                            image_path = linked_node.image.filepath.strip().lstrip("//")
                            index = texture_add(json_model,image_path)
                            
                            SC_shader_var[input_socket.name]={
                                 "index": index
                            }
                            print(input_socket.name,SC_shader_var[input_socket.name])
                        else:
                            print(input_socket.name," : ",linked_node)
                    else:
                        print(input_socket.type)
                        match input_socket.type:
                            case 'VECTOR':
                                 SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2]]
                            case 'VALUE':
                                SC_shader_var[input_socket.name]=input_socket.default_value
                        print(input_socket.name, input_socket.default_value)
            print(temp_material)
            json_model["materials"].append(temp_material)
def texture_add(json_model,texture_path):
    if("/" not in texture_path):
        texture_path="sc3d/"+texture_path
    for i in range(len(json_model["textures"])):
        if json_model["textures"][i]==texture_path:
            return i

    length =len(json_model["textures"])
    json_model["textures"].append({
        "source": length,
        "sampler": length
    })
    json_model["images"].append({
        "uri": texture_path.replace(".png",".ktx"),
    })
    return length

def glb2gltf(path: str):
	parser = GlbParser(path)
	parser.parse()
	
def gltf2glb(path: str):
	encoder = GlbEncoder(path)
	encoder.encode()

# 运行插件
if __name__ == "__main__":
    register()