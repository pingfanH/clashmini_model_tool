import bpy
import os
from clashmini_model_tools.materials import material as SC_Material
from clashmini_model_tools.utils.glb import GlbParser
from clashmini_model_tools.utils.glb import GlbEncoder

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
            temp_material = SC_Material.copy()
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
                            image_path=os.path.basename(linked_node.image.filepath)
                            print("Image Path:", image_path)
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
                                if(input_socket.name.endswith("_vector")):
                                    SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2]]
                                else:
                                    SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2]]
                            case 'VALUE':
                                if(input_socket.name.endswith("_alpha")):
                                    SC_shader_var[input_socket.name][3]=input_socket.default_value
                                else:
                                    SC_shader_var[input_socket.name]=input_socket.default_value
                            case _:
                                SC_shader_var[input_socket.name]=input_socket.default_value
                            
                        print(input_socket.name, input_socket.default_value)
            print(temp_material)
            json_model["materials"].append(temp_material)
def texture_add(json_model,texture_path):
    image = -1;
    if("/" not in texture_path):
        texture_path="sc3d/"+texture_path
    for i in range(len(json_model["textures"])):
        if json_model["images"][i]["uri"]==texture_path:
            image = i
    result=None;
    if image == -1:
        json_model["images"].append({
            "uri": texture_path.replace(".png",".ktx"),
        })
        textures_length =len(json_model["textures"])
        json_model["textures"].append({
            "source": len(json_model["images"]),
            "sampler": textures_length
        })
        result= textures_length
    else:
        print("Same Image :"+json_model["images"][i]["uri"]);
        textures_length =len(json_model["textures"])
        json_model["textures"].append({
            "source": image,
            "sampler": textures_length
        })
        result= textures_length
    print("texture "+{
            "source": image,
            "sampler": result
        })
    print("image "+json_model["images"][json_model["textures"][result]["source"]]["uri"])
    return result
def glb2gltf(path: str):
	parser = GlbParser(path)
	parser.parse()
	
def gltf2glb(path: str):
	encoder = GlbEncoder(path)
	encoder.encode()
