import bpy
import os
from clashmini_model_tools.materials import new_sc_material
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
            print(material.name)
            _material = new_sc_material()
            _sc_shader = _material["extensions"]["SC_shader"]
            _sc_shader["name"] = material.name
            SC_shader_var=_sc_shader["variables"]
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
                            #filepath=linked_node.image.filepath;
                            image_name = remove_before_last_backslash(linked_node.image.filepath)
                            print("------linked_node.image.filepath:"+image_name)
                            # if "filepath://" in filepath:
                            #     filepath = filepath.replace("filepath://","")
                            #image_path=#remove_before_last_backslash(filepath)#os.path.basename(linked_node.image.filepath)
                            #print("Image Path:", image_name)
                            index = texture_add(json_model,image_name)
                            
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
                                if len(input_socket.default_value) == 4:
                                    SC_shader_var[input_socket.name]=input_socket.default_value
                                elif input_socket.name.endswith("_vector"):
                                    SC_shader_var[replace_end(input_socket.name,"_vector","")]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2],0]
                                else:
                                    SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2]]
                                # if(input_socket.name.endswith("_vector")):
                                #     SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2]]
                                # else:
                                #     SC_shader_var[input_socket.name]=input_socket.default_value
                            case 'VALUE':
                                if(input_socket.name.endswith("_alpha")):
                                    SC_shader_var[replace_end(input_socket.name,"_alpha","")][3]=input_socket.default_value
                                else:
                                    SC_shader_var[input_socket.name]=input_socket.default_value
                            case 'RGBA':
                                SC_shader_var[input_socket.name]=[input_socket.default_value[0], input_socket.default_value[1], input_socket.default_value[2],input_socket.default_value[3]]
                            case _:
                                SC_shader_var[input_socket.name]=input_socket.default_value
                            
                        print(input_socket.name, input_socket.default_value)
            _sc_shader["variables"]=SC_shader_var
            _material["extensions"]["SC_shader"]=_sc_shader
            #print(temp_material)
            json_model["materials"].append(_material)

def texture_add(json_model,texture_path):
    print("texture_path:"+texture_path)
    image = -1;
    if("/" not in texture_path):
        texture_path="sc3d/"+texture_path
    for i in range(len(json_model["textures"])):
        if json_model["images"][i]["uri"]==texture_path:
            image = i
    result=None;
    if image == -1:
        textures_length =len(json_model["textures"])
        json_model["textures"].append({
            "source": len(json_model["images"]),
            "sampler": textures_length
        })
        json_model["images"].append({
            "uri": texture_path.replace(".png",".ktx"),
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
    #print("texture "+"source "+str(image) +"sampler"+str(result))
    #print("image "+json_model["images"][json_model["textures"][result]["source"]]["uri"])
    return result
def glb2gltf(path: str):
	parser = GlbParser(path)
	parser.parse()
	
def gltf2glb(path: str):
	encoder = GlbEncoder(path)
	encoder.encode()

def replace_end(original_str, old_end, new_end):
    if original_str.endswith(old_end):
        return original_str[:-len(old_end)] + new_end
    else:
        return original_str
def remove_before_last_backslash(string):
    index = string.rfind('\\')
    if index != -1:  # If backslash is found
        return string[index + 1:]
    else:
        return string
