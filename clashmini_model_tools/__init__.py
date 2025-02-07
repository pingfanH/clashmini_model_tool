import bpy
from clashmini_model_tools.exporter import ModelExport
from clashmini_model_tools.importer import ModelImport
from clashmini_model_tools.animation import AnimationExport
from clashmini_model_tools.utils.clashmini import clash_mini_model,material_convert,texture_add,glb2gltf,gltf2glb
bl_info = {
    "name": "Clash-mini-Tools",
    "description": "Tool For ClashMini Models",
    "author": "Pingfanh",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    #"warning": "This addon is still in development.",
    "wiki_url": "https://github.com/pingfanH",
    "category": "3D View"
}


class ExporterPanel(bpy.types.Panel):
    bl_label = bl_info["name"]
    bl_idname = "Exporter_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = bl_info["name"]
    def draw(self, context):
        layout = self.layout

        scene = context.scene

        row = layout.row()
        row.label(text=bl_info["name"]+" version-1.0.0", icon='WORLD_DATA')
        
        row = layout.row()
        row.label(text="ModelPath:")
        
        row = layout.row()
        row.prop(scene, "export_model_path", text="")
        
        row = layout.row()
        row.operator("item.model_export",text="Export", icon='MESH_CUBE')

        row = layout.row()
        row.label(text="Sc3dPath:")
        
        row = layout.row()
        row.prop(scene, "sc3d_path", text="")

        row = layout.row()
        row.label(text="ModelPath:")
        
        row = layout.row()
        row.prop(scene, "import_model_path", text="")
        
        row = layout.row()
        row.operator("item.model_import",text="Import", icon='MESH_CUBE')

        box = layout.box()
        box.scale_y = 0.1  # 控制高度

        row = layout.row()
        row.label(text="Animation:")

        row = layout.row()
        row.prop(scene, "animation_path", text="")

        row = layout.row()
        row.label(text="Path2:")

        row = layout.row()
        row.prop(scene, "animation_path1", text="")

        row.label(text="Prefix:")
        row = layout.row()
        row.prop(scene, "animation_path_prefix", text="")

        row = layout.row()
        row.operator("item.animation_export",text="Export", icon='MESH_CUBE')



# 注册自定义节点
def register():
    bpy.utils.register_class(ExporterPanel)
    bpy.utils.register_class(ModelExport)
    bpy.utils.register_class(ModelImport)
    bpy.utils.register_class(AnimationExport)
    bpy.types.Scene.export_model_path = bpy.props.StringProperty(
        name="Export Model Path",
        default=""
    )
    bpy.types.Scene.import_model_path = bpy.props.StringProperty(
        name="Import Model Path",
        default=""
    )
    bpy.types.Scene.sc3d_path = bpy.props.StringProperty(
        name="Sc3d Path",
        default=""
    )
    bpy.types.Scene.animation_path = bpy.props.StringProperty(
        name="Animation Path",
        default=""
    )
    bpy.types.Scene.animation_path1 = bpy.props.StringProperty(
        name="Animation Path1",
        default=""
    )
    bpy.types.Scene.animation_path_prefix = bpy.props.StringProperty(
        name="Animation Path Prefix",
        default=""
    )

# 注销自定义节点
def unregister():
    # 删除自定义属性，确保先清理引用关系
    # if hasattr(bpy.types.Scene, "export_model_path"):
    #     del bpy.types.Scene.export_model_path
    # if hasattr(bpy.types.Scene, "import_model_path"):
    #     del bpy.types.Scene.import_model_path
    # if hasattr(bpy.types.Scene, "sc3d_path"):
    #     del bpy.types.Scene.sc3d_path

    # 注销类
    for cls in [ExporterPanel, ModelExport, ModelImport,AnimationExport]:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError as e:
            print(f"Error unregistering {cls}: {e}")
    # del bpy.types.Scene.export_model_path
    # del bpy.types.Scene.import_model_path
    # del bpy.types.Scene.sc3d_path

def update_export_path(self, context):
    # Save the text value to a persistent location
    # For example, you could use Blender's user preferences
    bpy.context.user_preferences.addons[__name__].preferences.export_model_path = self.export_model_path

def update_import_path(self, context):

    bpy.context.user_preferences.addons[__name__].preferences.import_model_path = self.import_model_path
def update_animation_path(self, context):

    bpy.context.user_preferences.addons[__name__].preferences.animation_path = self.animation_path
    bpy.context.user_preferences.addons[__name__].preferences.animation_path1 = self.animation_path1
    bpy.context.user_preferences.addons[__name__].preferences.animation_path_prefix = self.animation_path_prefix


def load_text():
    # Load the text value from a persistent location
    # For example, you could use Blender's user preferences
    return bpy.context.user_preferences.addons[__name__].preferences.export_model_path

# 运行插件
if __name__ == "__main__":
    register()