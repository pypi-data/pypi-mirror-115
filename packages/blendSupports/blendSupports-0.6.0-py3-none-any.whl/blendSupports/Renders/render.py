from miscSupports import tuple_convert
from pathlib import Path
import bpy


class EngineInvalidError(Exception):
    """Invalid engine"""
    def __init__(self, engine):
        super().__init__(f"Engine takes the value of 'CYCLES' or 'BLENDER_EEVEE' yet found {engine}")


class CameraTypeError(Exception):
    """Invalid Camera"""
    def __init__(self, camera_type):
        super().__init__(f"Camera Type takes the value of 'PANO', 'ORTHO', or 'PERSP' yet found {camera_type}")


def render_scene(camera_position, write_directory, write_name, engine="CYCLES", x_resolution=1080,
                 y_resolution=1080, camera_type="ORTHO", camera_scale=5, save_file=True):

    if engine.upper() not in ["CYCLES", "BLENDER_EEVEE"]:
        raise EngineInvalidError(engine.upper())

    bpy.context.scene.render.engine = engine

    # Set the output resolution and camera scale
    bpy.context.scene.render.resolution_x = int(x_resolution)
    bpy.context.scene.render.resolution_y = int(y_resolution)

    # Set the camera position and scale
    camera = bpy.data.objects["Camera"]

    if camera_type.upper() not in ['PANO', "ORTHO", "PERSP"]:
        raise CameraTypeError(camera_type.upper())

    camera.data.type = camera_type.upper()
    camera.location = tuple_convert(camera_position)
    if camera_type == "ORTHO":
        camera.data.ortho_scale = float(camera_scale)

    # Render the scene
    bpy.context.scene.render.filepath = str(Path(write_directory, f"{write_name}.png").absolute())
    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still=True)

    if save_file:
        # Save the blend file for manual manipulation later
        bpy.ops.wm.save_as_mainfile(filepath=f"{write_directory}/{write_name}.blend")


render_scene((0, 0, 2), r"C:\Users\Samuel\PycharmProjects\blendSupports\Tests", "TR")