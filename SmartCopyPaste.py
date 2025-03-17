import bpy

bl_info = {
    "name": "SmartCopyPaste",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Umar Razzaq",
    "version": (1, 0),
    "description": "Copy and Paste object transforms, modifiers, materials, constraints, parenting, and custom properties.",
}

# Storage for copied values
copied_data = {
    "transforms": {}, 
    "modifiers": [], 
    "materials": [], 
    "constraints": [], 
    "parent": None, 
    "custom_properties": {}
}

# Copy Functions
def copy_transform(obj, transform_type):
    if obj:
        copied_data["transforms"][transform_type] = getattr(obj, transform_type).copy()
        return f"{transform_type.capitalize()} copied"
    return "No object selected"

def paste_transform(obj, transform_type):
    if obj and transform_type in copied_data["transforms"]:
        setattr(obj, transform_type, copied_data["transforms"][transform_type])
        return f"{transform_type.capitalize()} pasted"
    return "No object selected or nothing copied"

def copy_modifiers(obj):
    copied_data["modifiers"] = [(mod.name, mod.type) for mod in obj.modifiers]
    return "Modifiers copied"

def paste_modifiers(obj):
    for mod_name, mod_type in copied_data["modifiers"]:
        mod = obj.modifiers.new(name=mod_name, type=mod_type)
    return "Modifiers pasted"

def copy_materials(obj):
    copied_data["materials"] = [mat for mat in obj.data.materials]
    return "Materials copied"

def paste_materials(obj):
    obj.data.materials.clear()
    for mat in copied_data["materials"]:
        obj.data.materials.append(mat)
    return "Materials pasted"

def copy_constraints(obj):
    copied_data["constraints"] = [(con.name, con.type) for con in obj.constraints]
    return "Constraints copied"

def paste_constraints(obj):
    for con_name, con_type in copied_data["constraints"]:
        con = obj.constraints.new(type=con_type)
        con.name = con_name
    return "Constraints pasted"

def copy_parent(obj):
    copied_data["parent"] = obj.parent
    return "Parent copied"

def paste_parent(obj):
    obj.parent = copied_data["parent"]
    return "Parent pasted"

def copy_custom_properties(obj):
    copied_data["custom_properties"] = obj.items()
    return "Custom properties copied"

def paste_custom_properties(obj):
    for key, value in copied_data["custom_properties"]:
        obj[key] = value
    return "Custom properties pasted"

# Operators
class OBJECT_OT_CopyData(bpy.types.Operator):
    bl_idname = "object.copy_data"
    bl_label = "Copy Data"
    bl_description = "Copy object properties"
    data_type: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.active_object
        func = globals().get(f"copy_{self.data_type}")
        if obj and func:
            self.report({'INFO'}, func(obj))
        return {'FINISHED'}

class OBJECT_OT_PasteData(bpy.types.Operator):
    bl_idname = "object.paste_data"
    bl_label = "Paste Data"
    bl_description = "Paste copied properties to selected objects"
    data_type: bpy.props.StringProperty()

    def execute(self, context):
        func = globals().get(f"paste_{self.data_type}")
        if func:
            for obj in context.selected_objects:
                func(obj)
            self.report({'INFO'}, f"{self.data_type.capitalize()} applied to selected objects")
        return {'FINISHED'}

# UI Panel
class VIEW3D_PT_CopyPastePanel(bpy.types.Panel):
    bl_label = "SmartCopyPaste"
    bl_idname = "VIEW3D_PT_CopyPastePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SmartCopyPaste"

    def draw(self, context):
        layout = self.layout
        for data_type in ["transform", "modifiers", "materials", "constraints", "parent", "custom_properties"]:
            row = layout.row()
            row.operator("object.copy_data", text=f"Copy {data_type.capitalize()}").data_type = data_type
            row.operator("object.paste_data", text=f"Paste {data_type.capitalize()}").data_type = data_type

# Register
classes = [OBJECT_OT_CopyData, OBJECT_OT_PasteData, VIEW3D_PT_CopyPastePanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
