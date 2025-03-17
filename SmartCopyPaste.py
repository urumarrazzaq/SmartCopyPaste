import bpy

bl_info = {
    "name": "SmartCopyPaste",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Umar Razzaq",
    "version": (1, 0),
    "description": "Copy and Paste object transforms (location, rotation, scale)",
}

# Storage for copied values
copied_data = {}

def copy_transform(obj, transform_type):
    if obj:
        copied_data[transform_type] = getattr(obj, transform_type).copy()
        return f"{transform_type.capitalize()} copied"
    return "No object selected"

def paste_transform(obj, transform_type):
    if obj and transform_type in copied_data:
        setattr(obj, transform_type, copied_data[transform_type])
        return f"{transform_type.capitalize()} pasted"
    return "No object selected or nothing copied"

# Operators
class OBJECT_OT_CopyTransform(bpy.types.Operator):
    bl_idname = "object.copy_transform"
    bl_label = "Copy Transform"
    bl_description = "Copy the selected object's transform"
    transform_type: bpy.props.StringProperty()

    def execute(self, context):
        self.report({'INFO'}, copy_transform(context.active_object, self.transform_type))
        return {'FINISHED'}

class OBJECT_OT_PasteTransform(bpy.types.Operator):
    bl_idname = "object.paste_transform"
    bl_label = "Paste Transform"
    bl_description = "Paste the copied transform to selected objects"
    transform_type: bpy.props.StringProperty()

    def execute(self, context):
        for obj in context.selected_objects:
            paste_transform(obj, self.transform_type)
        self.report({'INFO'}, f"{self.transform_type.capitalize()} applied to selected objects")
        return {'FINISHED'}

# UI Panel
class VIEW3D_PT_CopyPastePanel(bpy.types.Panel):
    bl_label = "SmartCopyPaste Transform"
    bl_idname = "VIEW3D_PT_CopyPastePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SmartCopyPaste"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.copy_transform", text="Copy Location").transform_type = "location"
        row.operator("object.paste_transform", text="Paste Location").transform_type = "location"
        row = layout.row()
        row.operator("object.copy_transform", text="Copy Rotation").transform_type = "rotation_euler"
        row.operator("object.paste_transform", text="Paste Rotation").transform_type = "rotation_euler"
        row = layout.row()
        row.operator("object.copy_transform", text="Copy Scale").transform_type = "scale"
        row.operator("object.paste_transform", text="Paste Scale").transform_type = "scale"

# Register
classes = [OBJECT_OT_CopyTransform, OBJECT_OT_PasteTransform, VIEW3D_PT_CopyPastePanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()