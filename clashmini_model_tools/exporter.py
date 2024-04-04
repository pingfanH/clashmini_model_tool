import bpy
import json
import os
from clashmini_model_tools.utils.clashmini import clash_mini_model,material_convert,texture_add,gltf2glb
class ModelExport(bpy.types.Operator):
    bl_idname = "item.model_export"
    bl_label = "Export Model"
    #bl_description = "Rename all mesh UV maps to the same, by this u can join meshes into one without losing UV"
    #id: bpy.props.IntProperty(name="id", default=0) # type: ignore
    def execute(self, context):
        scene = bpy.context.scene
        output_path = scene.export_model_path
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
