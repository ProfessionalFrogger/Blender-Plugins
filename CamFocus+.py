bl_info = {
    "name": "CamFocus+", # Remove "Dev" at launch
    "blender": (4, 3, 2),
    "category": "3D View",
    "author": "ProfessionalFrogger",
    "description": "Switch to camera perspectives from a list.",
    "version": (1, 0, 4),
    "support": "Discord=https://discord.gg/JBxHRepG",
}

import bpy

# Operator to tolggle lock_camera
class LockCameraOperator(bpy.types.Operator):
    bl_idname = "view3d.toggle_lock_camera"
    bl_label = "Toggle Lock Camera"
    
    def excecute(self, context):
        context.space_data.lock_camera = not context.space_data.lock_camera
        return {'FINISHED'}

# START_CleanView
class CleanViewOperator(bpy.types.Operator):
# view3d.view_center_camera
    bl_idname = "view3d.view_center_camera_operator"
    bl_label = "Clean View"
    
    def execute(self, context):
        scene = context.scene
        
        bpy.ops.view3d.view_center_camera()
        bpy.context.object.data.show_passepartout = True
        bpy.context.object.data.passepartout_alpha = 1
        bpy.context.space_data.show_gizmo = False
        bpy.context.space_data.overlay.show_overlays = False
        context.area.spaces.active.show_region_toolbar = False
        #bpy.context.object.data.show_limits = True # Works, I just don't want it yet...
        #bpy.context.object.data.show_name = True # Probably works. Conflicts with show.gizmo

        ### START Test
        
        ### END Test

        return {'FINISHED'}
# END_ViewCenterCamera

# Operator to switch to the selected camera view
class VIEW3D_OT_CameraFocus(bpy.types.Operator):
    bl_idname = "view3d.camera_focus"
    bl_label = "Focus on Camera"

    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        # Find the camera by name
        scene = context.scene
        
        # find the camera object in the hiearchy that you want to 'view' from your gui menu
        camera = bpy.data.objects.get(self.camera_name)

        if camera and camera.type == 'CAMERA':
            # Set the active camera to the one selected
            scene.camera = camera
            
            # Selects desired Camera. Only took all night to figure this out...
            bpy.ops.object.select_all(action='DESELECT')
            camera.select_set(True)
            bpy.context.view_layer.objects.active = camera
            
            #area = areas.get("VIEW_3D",None)
            
            active_area = context.area
            if active_area.type == 'VIEW_3D':
                region_3d = active_area.spaces[0].region_3d
                space = active_area.spaces.active
                if space:
                    space.region_3d.view_perspective = 'CAMERA'
                    
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, f"No camera named {self.camera_name} found")
            return {'CANCELLED'}

# Panel to display the list of cameras
class VIEW3D_PT_CamFocusPanel(bpy.types.Panel):
    bl_label = "CamFocus+" # Remove "Dev" at launch
    bl_idname = "VIEW3D_PT_cam_focus_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CamFocus+' # Remove "Dev" at launch

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # checkbox for lock_camera
        layout.prop(context.space_data, "lock_camera", text="Lock Camera") # checkbox for lock_camera
        
        # button for view_center_camera
        layout.operator(CleanViewOperator.bl_idname, text="Clean View")
        
        # Create a list of cameras in the scene
        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
        
        # Add a button for each camera
        for camera in cameras:
            layout.operator("view3d.camera_focus", text=camera.name).camera_name = camera.name

# Register the classes
def register():
    #
    bpy.utils.register_class(VIEW3D_OT_CameraFocus)
    bpy.utils.register_class(VIEW3D_PT_CamFocusPanel)
    
    # 
    bpy.utils.register_class(LockCameraOperator)
    
    #
    bpy.utils.register_class(CleanViewOperator)
    #bpy.types.VIEW3D_PT_view.append(draw_func)
    

def unregister():
    #
    bpy.utils.unregister_class(VIEW3D_OT_CameraFocus)
    bpy.utils.unregister_class(VIEW3D_PT_CamFocusPanel)
    
    #
    bpy.utils.unregister_class(LockCameraOperator)
    
    #
    bpy.utils.unregister_class(CleanViewOperator)
    #bpy.types.VIEW3D_PT_view.remove(draw_func)

if __name__ == "__main__":
    register()




###   Things to add:   ###



