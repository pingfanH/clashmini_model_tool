import bpy

# class CustomGroup:
#     custom_group:bpy.data.node_groups;
#     index=0

#     def __init__(self,obj=None) -> None:
#         self.custom_group=bpy.data.node_groups.new(name="Custom Group", type='ShaderNodeTree')
#         self.socket_input=self.custom_group.nodes.new('NodeGroupInput')
#         self.socket_input.location = (-300, 100)
#         self.bsdf_node=self.custom_group.nodes.new(type="ShaderNodeBsdfPrincipled")
              
#         self.float_input("IOR",16)
#         self.vector_input("Tangent",24)
#         self.vector_input("ambient")
#         self.float_input("ambientIntensity")
#         self.color_input("diffuseTex2D",0)
#         self.float_input("directRadianceStrength")
#         self.vector_input("emission")
#         self.float_input("emissionStrength")
#         self.bool_input("enableEmissionTex")
#         self.bool_input("enableFresnel")
#         self.bool_input("enableGammaCorrection")
#         self.bool_input("enableHDR")
#         self.bool_input("enableMRA")
#         self.bool_input("enableMainUVAnim")
#         self.bool_input("enableReflection")
#         self.bool_input("enableResetScale")
#         self.bool_input("enableSSS")
#         self.bool_input("enableSceneFlag")
#         self.bool_input("enableStencil")
#         self.bool_input("enableUVAnim")
#         self.bool_input("enableUVAnimMultiply")
#         self.quaternion_input("fresnelColor")
#         self.float_input("fresnelMask")
#         self.float_input("fresnelStrength")
#         self.quaternion_input("lightColor")
#         self.vector_input("lightDir")
#         self.color_input("lightFlowMaskTex2D")
#         self.color_input("lightFlowTex2D")
#         self.float_input("metalness")
#         self.color_input("mraTex2D")
#         self.vector_input("normal")
#         self.quaternion_input("opacity")
#         self.color_input("reflectioinTex2D")
#         self.float_input("roughness")
#         self.float_input("specularStrength")
#         self.color_input("sssMaskTex2D")
#         self.float_input("sssStrength")
#         self.color_input("sssTex2D")
#         self.vector_input("stencilOffset")
#         self.vector_input("stencilScale")
#         self.color_input("stencilTex2D")
#         self.quaternion_input("teamColor")
#         self.color_input("teamColorTex2D")
#         self.vector_input("textureUV")
#         self.vector_input("textureUV2")
#         self.bool_input("u_convertTosRGB_maya")
#         self.bool_input("u_convertsrgb_maya")
#         self.vector_input("uvSpeedAnim")
#         selected_object =obj;
#         if obj is None:
#             selected_object = bpy.context.selected_objects[0]
#         material = selected_object.material_slots[0].material
#         output_bsdf = self.custom_group.nodes.new('NodeGroupOutput')
#         output_bsdf.location = (300, 100)  # 设置输出节点的位置
#         output_bsdf.name = 'Output'
#         self.custom_group.outputs.new('NodeSocketShader', output_bsdf.name)

#         # 链接节点
#         self.custom_group.links.new(self.bsdf_node.outputs[0], output_bsdf.inputs[0])

#         # 将新创建的节点组链接到材质中
#         shader_node_tree = material.node_tree
#         custom_group_node = shader_node_tree.nodes.new(type="ShaderNodeGroup")
#         custom_group_node.node_tree = self.custom_group

#         material_output = shader_node_tree.nodes.new('ShaderNodeOutputMaterial')
#         material_output.location = (300, 100)
#         shader_node_tree.links.new(custom_group_node.outputs['Output'], material_output.inputs['Surface'])

    
#     def float_input(self,name,output=-1):
#         # _float=self.custom_group.nodes.new('NodeGroupInput')
#         # _float.location = (-300, 100)
#         # _float.name = name
#         self.custom_group.inputs.new('NodeSocketFloat', name)
#         if output!=-1:
#             self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])

#         self.index+=1;
#     def vector_input(self,name,output=-1):
#         # _array = self.custom_group.nodes.new('NodeGroupInput')
#         # _array.location = (-300, 100)
#         # _array.name =name
#         self.custom_group.inputs.new('NodeSocketVector',name)
#         if output!=-1:
#             self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
#         self.index+=1;
#     def quaternion_input(self,name,output=-1):
#         # _array = self.custom_group.nodes.new('NodeGroupInput')
#         # _array.location = (-300, 100)
#         # _array.name =name
#         self.custom_group.inputs.new('NodeSocketVector',name)
#         self.custom_group.inputs.new('NodeSocketFloat',name)
#         if output!=-1:
#             self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
#         self.index+=2;
#     def color_input(self,name,output=-1):
#         # _color = self.custom_group.nodes.new('NodeGroupInput')
#         # _color.location = (-300, 100)
#         # _color.name =name
#         print(self.index)
#         self.custom_group.inputs.new('NodeSocketColor',name)
#         if output!=-1:
#             self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
#         self.index+=1;
#     def bool_input(self,name,output=-1):
#         # _bool = self.custom_group.nodes.new('NodeGroupInput')
#         # _bool.location = (-300, -50)  # 设置输入节点的位置
#         # _bool.name = name
#         self.custom_group.inputs.new('NodeSocketBool', name)
#         if output!=-1:
#             self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
#         self.index+=1;

# if __name__ == "__main__":
#     group = CustomGroup()

class CustomGroup:
    #custom_group:bpy.data.node_groups;
    index=0;
    images_load_index=0;

    def __init__(self,material=None) -> None:
        # selected_object =obj;
        if material is None:
            #selected_object = bpy.context.selected_objects[0]
            return
        # material = selected_object.material_slots[0].material
        self.shader_node_tree = material.node_tree
        for node in self.shader_node_tree.nodes:
            self.shader_node_tree.nodes.remove(node)
        
        self.custom_group=bpy.data.node_groups.new(name="Custom Group", type='ShaderNodeTree')
        self.socket_input=self.custom_group.nodes.new('NodeGroupInput')
        self.socket_input.location = (-300, 100)
        self.bsdf_node=self.custom_group.nodes.new(type="ShaderNodeBsdfPrincipled")
              
        self.float_input("IOR",16)
        self.vector_input("Tangent",24)
        self.quaternion_input("ambient")
        self.float_input("ambientIntensity")
        self.color_input("diffuseTex2D",0)
        self.float_input("directRadianceStrength")
        self.quaternion_input("emission")
        self.float_input("emissionStrength")
        self.bool_input("enableEmissionTex")
        self.bool_input("enableFresnel")
        self.bool_input("enableGammaCorrection")
        self.bool_input("enableHDR")
        self.bool_input("enableMRA")
        self.bool_input("enableMainUVAnim")
        self.bool_input("enableReflection")
        self.bool_input("enableResetScale")
        self.bool_input("enableSSS")
        self.bool_input("enableSceneFlag")
        self.bool_input("enableStencil")
        self.bool_input("enableUVAnim")
        self.bool_input("enableUVAnimMultiply")
        self.quaternion_input("fresnelColor")
        self.float_input("fresnelMask")
        self.float_input("fresnelStrength")
        self.quaternion_input("lightColor")
        self.vector_input("lightDir")
        self.color_input("lightFlowMaskTex2D")
        self.color_input("lightFlowTex2D")
        self.float_input("metalness")
        self.color_input("mraTex2D")
        self.vector_input("normal")
        self.quaternion_input("opacity")
        self.color_input("reflectioinTex2D")
        self.float_input("roughness")
        self.float_input("specularStrength")
        self.color_input("sssMaskTex2D")
        self.float_input("sssStrength")
        self.color_input("sssTex2D")
        self.vector_input("stencilOffset")
        self.vector_input("stencilScale")
        self.color_input("stencilTex2D")
        self.quaternion_input("teamColor")
        self.color_input("teamColorTex2D")
        self.vector_input("textureUV")
        self.vector_input("textureUV2")
        self.bool_input("u_convertTosRGB_maya")
        self.bool_input("u_convertsrgb_maya")
        self.vector_input("uvSpeedAnim")
        
        output_bsdf = self.custom_group.nodes.new('NodeGroupOutput')
        output_bsdf.location = (300, 100)  # 设置输出节点的位置
        output_bsdf.name = 'Output'
        self.custom_group.outputs.new('NodeSocketShader', output_bsdf.name)

        # 链接节点
        self.custom_group.links.new(self.bsdf_node.outputs[0], output_bsdf.inputs[0])

        # 将新创建的节点组链接到材质中
        custom_group_node = self.shader_node_tree.nodes.new(type="ShaderNodeGroup")
        custom_group_node.node_tree = self.custom_group
        self.custom_group_node=custom_group_node
        material_output = self.shader_node_tree.nodes.new('ShaderNodeOutputMaterial')
        material_output.location = (300, 100)
        self.shader_node_tree.links.new(custom_group_node.outputs['Output'], material_output.inputs['Surface'])
        
    def add_texture_node(self, image_path, node_name="Texture"):
        texture_node = self.shader_node_tree.nodes.new(type="ShaderNodeTexImage")
        texture_node.location = (-400, -400*self.images_load_index)  # 设置节点的位置
        self.images_load_index+=1;
        texture_node.image = bpy.data.images.load(bpy.context.scene.sc3d_path+"/"+image_path.split("/")[-1])    # 加载纹理图片
        texture_node.name = node_name
        return texture_node
    def connect_texture_to_color(self, texture_node, color_input_name):
        color_input = self.custom_group_node.inputs.get(color_input_name)
        if color_input:
            self.shader_node_tree.links.new(texture_node.outputs["Color"], color_input)
        else:
            print("Color input socket", color_input_name, "not found.")
    def float_input(self,name,output=-1):
        # _float=self.custom_group.nodes.new('NodeGroupInput')
        # _float.location = (-300, 100)
        # _float.name = name
        self.custom_group.inputs.new('NodeSocketFloat', name)
        if output!=-1:
            self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])

        self.index+=1;
    def vector_input(self,name,output=-1):
        # _array = self.custom_group.nodes.new('NodeGroupInput')
        # _array.location = (-300, 100)
        # _array.name =name
        self.custom_group.inputs.new('NodeSocketVector',name)
        if output!=-1:
            self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
        self.index+=1;
    def quaternion_input(self,name,output=-1):
        # _array = self.custom_group.nodes.new('NodeGroupInput')
        # _array.location = (-300, 100)
        # _array.name =name
        # self.custom_group.inputs.new('NodeSocketVector',name)
        # self.custom_group.inputs.new('NodeSocketFloat',name)
        # if output!=-1:
        #     self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
        # self.index+=2;
        self.vector_input(name + "_vector", output)  # 添加 vector 类型的输入
        self.float_input(name + "_alpha", output)    # 添加浮点数类型的输入
        #self.index+=2;
    def color_input(self,name,output=-1):
        # _color = self.custom_group.nodes.new('NodeGroupInput')
        # _color.location = (-300, 100)
        # _color.name =name
        print(self.index)
        self.custom_group.inputs.new('NodeSocketColor',name)
        if output!=-1:
            self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
        self.index+=1;
    def bool_input(self,name,output=-1):
        # _bool = self.custom_group.nodes.new('NodeGroupInput')
        # _bool.location = (-300, -50)  # 设置输入节点的位置
        # _bool.name = name
        self.custom_group.inputs.new('NodeSocketBool', name)
        if output!=-1:
            self.custom_group.links.new(self.socket_input.outputs[self.index], self.bsdf_node.inputs[output])
        self.index+=1;
    def rgba_input(self, name, output=-1):
        self.vector_input(name + "_vector", output)  # 添加 vector 类型的输入
        self.float_input(name + "_alpha", output)    # 添加浮点数类型的输入
        self.index+=2;
    def set_socket(self, name, value):
        # 获取要设置值的输入
        input_socket = self.custom_group_node.inputs.get(name)
        if input_socket is not None:
            print(input_socket.type)
            # 根据输入的类型设置新值
            print("Socket", name, "set to", value)
            if input_socket.type == 'VALUE':
                input_socket.default_value = value  # 用于 Float 和 Int 类型
            elif input_socket.type == 'VECTOR':
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
                path = json["images"][value["index"]]["uri"].split(".")[0]+".png"  # 获取纹理图片路径;
                path ="D:/BS/clash mini/brawl_mini/model_export_addon/"+path
                print("Texture path:", path)
                texture_node = self.add_texture_node(path)
                self.connect_texture_to_color(texture_node, name)
                #input_socket.default_value = value  # 用于 Color 类型
            elif input_socket.type == 'BOOLEAN':
                input_socket.default_value = value  # 用于 Boolean 类型
            else:
                print("Unsupported socket type:", input_socket.type)
        else:
            print("Socket with name", name, "not found.")
        