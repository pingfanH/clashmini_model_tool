import bpy
import json
import os
from clashmini_model_tools.utils.clashmini import clash_mini_model,material_convert,texture_add,gltf2glb
class AnimationExport(bpy.types.Operator):
    bl_idname = "item.animation_export"
    bl_label = "Export Animation"
    def execute(self, context):
        try:
            bpy.ops.anim.channels_select_all(action='SELECT')
            bpy.ops.nla.select_all(action='SELECT')
            bpy.ops.nla.tracks_delete()
        except:
            pass
        scene = bpy.context.scene
        animation_path = scene.animation_path
        animation_path1 = scene.animation_path1
        animation_path_prefix = scene.animation_path_prefix
        # 获取活动对象
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object found.")
            return {'CANCELLED'}

        # 确保对象是动画的类型
        if not obj.animation_data or not obj.animation_data.action:
            self.report({'ERROR'}, "The object has no animations.")
            return {'CANCELLED'}

        # 保存原始旋转
        original_rotation = obj.rotation_euler.copy()
        original_action = obj.animation_data.action
        # # 导出路径
        print("path:"+animation_path)
        print("path:"+animation_path1)
        # 创建导出目录（如果不存在）
        if not os.path.exists(animation_path):
            os.makedirs(animation_path)

        # 获取所有动画动作
        actions = bpy.data.actions
        for action in actions:
            for index,i in enumerate(actions):
                print(bpy.data.scenes["Scene"].gltf_action_filter[index].keep)
                print(i.name)
                if(i!=action):
                    bpy.data.scenes["Scene"].gltf_action_filter[index].keep=False
                else:
                    bpy.data.scenes["Scene"].gltf_action_filter[index].keep=True
            # 绑定动作到对象
            obj.animation_data.action = action
            
            # 旋转对象 90 度（沿 X轴）
            obj.rotation_euler = (original_rotation.x + 1.5708, original_rotation.y, original_rotation.z)  # 90 度 = π/2

            # 设置导出的文件名
            
            export_path= os.path.join(animation_path, f"{animation_path_prefix}{action.name}.glb")
            export_path1= os.path.join(animation_path1, f"{animation_path_prefix}{action.name}.glb")
            print("ani-path"+export_path)
            bpy.ops.object.select_all(action='DESELECT')  # 取消所有选择
            obj.select_set(True)  # 选择当前对象
            # 导出为 GLTF
            bpy.ops.export_scene.gltf(
                export_animations=True,
                filepath=export_path,
                export_format='GLB',
                use_selection=True,  # 仅导出选中的对象
                export_current_frame=False,  # 导出整个动作
                
                #export_anim_single_armature=True
                #export_animation=True,
            )
            if(os.path.exists(animation_path1)):
                bpy.ops.export_scene.gltf(
                export_animations=True,
                filepath=export_path1,
                export_format='GLB',
                use_selection=True,  # 仅导出选中的对象
                export_current_frame=False,)
                self.report({'INFO'}, f"Exported animation: {action.name} to {export_path1}")
            
            self.report({'INFO'}, f"Exported animation: {action.name} to {export_path}")
            

        # 恢复对象旋转
        obj.rotation_euler = original_rotation
        obj.animation_data.action = original_action
    
        return {'FINISHED'}