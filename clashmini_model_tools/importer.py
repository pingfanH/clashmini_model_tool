import bpy
from clashmini_model_tools.utils.glb import GlbParser
from clashmini_model_tools.utils.glb import GlbEncoder
from clashmini_model_tools.custom_group import CustomGroup

#file_path = "D:\\BS\\clash mini\\brawl_mini\\model_export_addon\\chr_barbarianking_rig.glb"

def glb2gltf(path: str):
    parser = GlbParser(path)
    json,data=parser.parse_return()
    return json
    

class ModelImport(bpy.types.Operator):
    bl_idname = "item.model_import"
    bl_label = "Import Model"
    def execute(self, context):
        scene = bpy.context.scene
        import_path = scene.import_model_path
        import_glb(import_path)
        return {'FINISHED'}

def import_glb(path):
    bpy.ops.import_scene.gltf(filepath=path,bone_heuristic='BLENDER')
    json = glb2gltf(path)
    
    def set_socket(self, name, value):
        # 获取要设置值的输入
        input_socket = self.custom_group_node.inputs.get(name)
        if input_socket is None:
            input_socket=self.custom_group_node.inputs.get(name+"_vector")
        if input_socket is not None:
            print(input_socket.type)
            # 根据输入的类型设置新值
            print("Socket", name, "set to", value)
            if input_socket.type == 'VALUE':
                input_socket.default_value = value  # 用于 Float 和 Int 类型
            elif input_socket.type == 'VECTOR':
                if isinstance(value, (int, float)):
                    list=[value,value,value]
                    input_socket.default_value =list
                    return
                if len(value) == 4:
                    input_vector = self.custom_group_node.inputs.get(name + "_vector")
                    input_alpha = self.custom_group_node.inputs.get(name + "_alpha")
                    input_vector.default_value = value[:3]  # 设置 vector 输入
                    input_alpha.default_value = value[3]    # 设置浮点数输入
                    return
                input_socket.default_value = value  # 用于 Vector 类型
            elif input_socket.type == 'RGBA':
                if(value==""):
                    return
                if(len(value) == 4):
                    input_socket.default_value = value
                    return
                image_index = json["textures"][value["index"]]["source"]
                
                path = json["images"][image_index]["uri"].split(".")[0]+".png"  # 获取纹理图片路径;
                path ="D:/BS/clash mini/brawl_mini/model_export_addon/"+path
                print("Texture path:", path)
                texture_node = self.add_texture_node(path)
                texture_node.image.name=json["images"][image_index]["uri"]
                self.connect_texture_to_color(texture_node, name)
                #input_socket.default_value = value  # 用于 Color 类型
            elif input_socket.type == 'BOOLEAN':
                input_socket.default_value = value  # 用于 Boolean 类型
            else:
                print("Unsupported socket type:", input_socket.type)
        else:
            print("Socket with name", name, "not found.")
        
    #selected_objects = bpy.data.objects
    selected_objects = bpy.context.selected_objects
    
    for index in range(len(json["meshes"])):
        mesh =json["meshes"][index]
        mesh_name = None
        if mesh.get("name") is not None:
            #mesh_name = mesh["name"].rsplit(".", 1)[0]
            for node_index in range(len(json["nodes"]) - 1, -1, -1):
                if json["nodes"][node_index].get("mesh") is not None and json["nodes"][node_index]["mesh"] == index:
                    mesh_name = json["nodes"][node_index]["name"]
        else:
            mesh_name="Mesh_"+str(index)

        # 检查场景中是否存在具有指定名称的对象
        for obj in selected_objects:
            print(mesh_name,obj.name.rsplit(".", 1)[0])
            found_object = None
            if mesh_name == obj.name.rsplit(".", 1)[0]:
                found_object = obj
            else:
                continue

            #if mesh["name"] in selected_objects:
            # 获取对象
            obj = found_object#selected_objects[mesh["name"]]
            for index in range(len(mesh["primitives"])):
                print("primitives",mesh["primitives"][index]["material"])
                material=obj.material_slots[index].material
                print(material.name)
                group = CustomGroup(material)

                sc_shader = json["materials"][
                    mesh["primitives"][index]["material"]
                    ]["extensions"]["SC_shader"]
                material.name=sc_shader["name"]
                variables=sc_shader["variables"]
                for key in variables:
                    set_socket(group,key,variables[key])
        else:
            print("Object with name", mesh["name"], "not found in the scene.")