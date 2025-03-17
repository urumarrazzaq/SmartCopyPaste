import bpy

bl_info = {
    "name": "SmartCopyPaste",
    "blender": (2, 80, 0),
    "category": "Object",
    "author": "Umar Razzaq",
    "version": (1, 1),
    "description": "Copy and Paste object transforms, modifiers, materials, constraints, parenting, and custom properties.",
}

# Storage for copied values
copied_data = {
    "location": None,
    "rotation": None,
    "scale": None,
    "modifiers": [],
    "materials": [],
    "constraints": [],
    "parent": None,
    "custom_properties": {},
}

# Copy-Paste Functions
def copy_data(obj, data_type):
    if obj:
        if data_type in ["location", "rotation", "scale"]:
            copied_data[data_type] = getattr(obj, data_type).copy()
        elif data_type == "modifiers":
            copied_data[data_type] = [(mod.name, mod.type) for mod in obj.modifiers]
        elif data_type == "materials":
            copied_data[data_type] = [mat for mat in obj.data.materials]
        elif data_type == "constraints":
            copied_data[data_type] = [(con.name, con.type) for con in obj.constraints]
        elif data_type == "parent":
            copied_data[data_type] = obj.parent
        elif data_type == "custom_properties":
            copied_data[data_type] = dict(obj.items())

        return f"{data_type.capitalize()} copied"
    return "No object selected"

def paste_data(obj, data_type):
    if obj and copied_data[data_type] is not None:
        if data_type in ["location", "rotation", "scale"]:
            setattr(obj, data_type, copied_data[data_type])
        elif data_type == "modifiers":
            for mod_name, mod_type in copied_data[data_type]:
                mod = obj.modifiers.new(name=mod_name, type=mod_type)
        elif data_type == "materials":
            obj.data.materials.clear()
            for mat in copied_data[data_type]:
                obj.data.materials.append(mat)
        elif data_type == "constraints":
            for con_name, con_type in copied_data[data_type]:
                con = obj.constraints.new(type=con_type)
                con.name = con_name
        elif data_type == "parent":
            obj.parent = copied_data[data_type]
        elif data_type == "custom_properties":
            for key, value in copied_data[data_type].items():
                obj[key] = value

        return f"{data_type.capitalize()} pasted"
    return "No object selected or nothing copied"

# Operators
class OBJECT_OT_CopyData(bpy.types.Operator):
    bl_idname = "object.copy_data"
    bl_label = "Copy Data"
    bl_description = "Copy selected object data"
    data_type: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.active_object
        if obj:
            self.report({'INFO'}, copy_data(obj, self.data_type))
        return {'FINISHED'}

class OBJECT_OT_PasteData(bpy.types.Operator):
    bl_idname = "object.paste_data"
    bl_label = "Paste Data"
    bl_description = "Paste copied data to selected objects"
    data_type: bpy.props.StringProperty()

    def execute(self, context):
        for obj in context.selected_objects:
            self.report({'INFO'}, paste_data(obj, self.data_type))
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

        # Transforms Section
        box = layout.box()
        box.label(text="Transforms", icon="OBJECT_DATA")
        row = box.row()
        row.operator("object.copy_data", text="Copy Location").data_type = "location"
        row.operator("object.paste_data", text="Paste Location").data_type = "location"

        row = box.row()
        row.operator("object.copy_data", text="Copy Rotation").data_type = "rotation"
        row.operator("object.paste_data", text="Paste Rotation").data_type = "rotation"

        row = box.row()
        row.operator("object.copy_data", text="Copy Scale").data_type = "scale"
        row.operator("object.paste_data", text="Paste Scale").data_type = "scale"

        # Modifiers Section
        box = layout.box()
        box.label(text="Modifiers", icon="MODIFIER")
        row = box.row()
        row.operator("object.copy_data", text="Copy Modifiers").data_type = "modifiers"
        row.operator("object.paste_data", text="Paste Modifiers").data_type = "modifiers"

        # Materials Section
        box = layout.box()
        box.label(text="Materials", icon="MATERIAL")
        row = box.row()
        row.operator("object.copy_data", text="Copy Materials").data_type = "materials"
        row.operator("object.paste_data", text="Paste Materials").data_type = "materials"

        # Constraints Section
        box = layout.box()
        box.label(text="Constraints", icon="CONSTRAINT")
        row = box.row()
        row.operator("object.copy_data", text="Copy Constraints").data_type = "constraints"
        row.operator("object.paste_data", text="Paste Constraints").data_type = "constraints"

        # Parenting Section
        box = layout.box()
        box.label(text="Parenting", icon="OUTLINER_OB_ARMATURE")
        row = box.row()
        row.operator("object.copy_data", text="Copy Parent").data_type = "parent"
        row.operator("object.paste_data", text="Paste Parent").data_type = "parent"

        # Custom Properties Section
        box = layout.box()
        box.label(text="Custom Properties", icon="PROPERTIES")
        row = box.row()
        row.operator("object.copy_data", text="Copy Custom Properties").data_type = "custom_properties"
        row.operator("object.paste_data", text="Paste Custom Properties").data_type = "custom_properties"

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
