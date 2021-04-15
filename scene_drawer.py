from model_drawer import ModelDrawer
from vpython import canvas
from PIL import ImageGrab
from data import Scene
import random
import time
import os


class SceneDrawer:
    screenshot_bounding_box = (8, 79, 508, 579)
    screenshot_wait_time = 0.15
    screenshot_folder = "img"
    screenshot_filename = "scene"
    images_to_generate = 10
    min_models_per_scene = 2
    max_models_per_scene = 4
    canvas_width = 500
    canvas_height = 500
    dummy_index = -1

    # initialize a SceneDrawer object by giving it a scene to wrap
    def __init__(self, my_scene):
        self.scene = my_scene

    # draws the models in the scene
    def draw(self):
        for model in self.scene.model_list:
            model_drawer = ModelDrawer(model)
            model_drawer.draw()

    @staticmethod
    def orchestrate():
        SceneDrawer.check_screenshot_directory()
        scene_list = SceneDrawer.generate_scenes()
        SceneDrawer.cleanup_dummy_image(scene_list)
        return scene_list

    # ensures that the directory to hold screenshots exists
    @staticmethod
    def check_screenshot_directory():
        if not os.path.isdir(SceneDrawer.screenshot_folder):
            os.mkdir(SceneDrawer.screenshot_folder)

    @staticmethod
    def generate_scenes():
        scene_list = []
        for scene_index in range(SceneDrawer.dummy_index, SceneDrawer.images_to_generate):
            scene_list.append(SceneDrawer.generate_random_scene(scene_index))
            SceneDrawer.draw_scene(scene_list[-1], scene_index)
        return scene_list

    @staticmethod
    def generate_random_scene(scene_index):
        scene = Scene()
        scene.model_list = []
        scene.image_location = SceneDrawer.find_image_location(scene_index)
        model_count = random.randint(SceneDrawer.min_models_per_scene, SceneDrawer.max_models_per_scene)
        vpython_location_set = set()  # to check for overlapping models
        model_index = 0
        while model_index < model_count:
            model = ModelDrawer.generate_random_model()
            if model.vpython_location not in vpython_location_set:
                vpython_location_set.add(model.vpython_location)
                scene.model_list.append(model)
                model_index += 1
        return scene

    # a single iteration of the loop in "generate_scenes"
    # steps:
    # (1) initialize a new, blank canvas
    # (2) draw the scene
    # (3) wait for vpython to finish drawing the scene
    # (4) screenshot the scene
    # (5) delete the canvas
    @staticmethod
    def draw_scene(my_scene, index):
        # (1) initialize canvas before drawing
        my_canvas = canvas(width=SceneDrawer.canvas_width, height=SceneDrawer.canvas_height)

        # (2) create our scene-drawing object, then draw
        scene_drawer = SceneDrawer(my_scene)
        scene_drawer.draw()

        # (3) let vpython catch up before we screenshot
        time.sleep(SceneDrawer.screenshot_wait_time)

        # (4) screenshot the scene
        my_scene.image_location = SceneDrawer.find_image_location(index)
        image_grab = ImageGrab.grab(SceneDrawer.screenshot_bounding_box)
        image_grab.save(my_scene.image_location)

        # (5) delete canvas
        my_canvas.delete()

    @staticmethod
    def cleanup_dummy_image(scene_list):
        os.remove(SceneDrawer.find_image_location(SceneDrawer.dummy_index))
        del scene_list[0]

    @staticmethod
    def find_image_location(index):
        return "{}/{}{}.jpg".format(SceneDrawer.screenshot_folder, SceneDrawer.screenshot_filename, index)


def main():
    return SceneDrawer.orchestrate()


if __name__ == "__main__":
    main()
