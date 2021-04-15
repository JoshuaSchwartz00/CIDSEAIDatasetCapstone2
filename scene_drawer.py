from model_drawer import ModelDrawer
from vpython import canvas
from PIL import ImageGrab
from data import Scene
import itertools
import pickle
import random
import time
import os


class SceneDrawer:
    screenshot_bounding_box = (8, 110, 506, 608)
    screenshot_wait_time = 0.15
    screenshot_folder = "img"
    screenshot_filename = "scene"
    pickle_folder = "pickle"
    pickle_filename = "scene_list"
    models_per_scene = range(2, 3)
    canvas_width = 500
    canvas_height = 500
    image_location_format = "{}/{}{}.jpg"
    pickle_path_format = "{}/{}.pickle"

    # maps vpython location to pixel location
    pixel_map = {(-2, 2, 0): (110, 86), (0, 2, 0): (250, 86), (2, 2, 0): (390, 86),
                 (-2, 0, 0): (110, 232), (0, 0, 0): (250, 232), (2, 0, 0): (390, 232),
                 (-2, -2, 0): (110, 378), (0, -2, 0): (250, 378), (2, -2, 0): (390, 378)}

    def __init__(self, my_scene):
        self.scene = my_scene

    def __str__(self):
        return str(self.scene)

    def draw(self):
        # (1) initialize canvas before drawing
        my_canvas = canvas(width=SceneDrawer.canvas_width, height=SceneDrawer.canvas_height)
        for model in self.scene.model_list:  # (2) draw every model
            model_drawer = ModelDrawer(model)
            model_drawer.draw()
        time.sleep(SceneDrawer.screenshot_wait_time)  # (3) let vpython catch up before we screenshot
        image_grab = ImageGrab.grab(SceneDrawer.screenshot_bounding_box)  # (4) screenshot the scene
        image_grab.save(self.scene.image_location)
        my_canvas.delete()  # (5) delete canvas

    def assign_image_location(self, index):
        self.scene.image_location = self.image_location_format.format(SceneDrawer.screenshot_folder,
                                                                      SceneDrawer.screenshot_filename, index)

    def assign_positions(self):
        vpython_locations = random.sample(SceneDrawer.pixel_map.keys(), len(self.scene.model_list))
        for model, vpython_location in zip(self.scene.model_list, vpython_locations):
            model.vpython_location = vpython_location
            model.normalized_location = SceneDrawer.compute_normalized_location(vpython_location)
            model.pixel_location = SceneDrawer.compute_pixel_location(vpython_location)

    @staticmethod
    def compute_normalized_location(vpython_location):
        normalized_x = (vpython_location[0] + 2) // 2
        normalized_y = (-1 * vpython_location[1] + 2) // 2
        return normalized_x, normalized_y

    @staticmethod
    def compute_pixel_location(vpython_location):
        return SceneDrawer.pixel_map[vpython_location]

    @staticmethod
    def orchestrate():
        SceneDrawer.ensure_directory_exists(SceneDrawer.screenshot_folder)
        scene_list = SceneDrawer.generate_scenes()
        SceneDrawer.ensure_directory_exists(SceneDrawer.pickle_folder)
        SceneDrawer.save_pickle(scene_list)

    @staticmethod
    def ensure_directory_exists(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def generate_permutations():
        scenes = []
        model_permutations = ModelDrawer.generate_permutations()
        for model_count in SceneDrawer.models_per_scene:
            model_product = itertools.product(model_permutations, repeat=model_count)
            for model_tuples in model_product:
                scene = Scene()
                scene.model_list = ModelDrawer.model_tuples_to_models(model_tuples)
                scenes.append(scene)
        return scenes

    @staticmethod
    def generate_scenes():
        scenes = SceneDrawer.generate_permutations()
        for index, my_scene in enumerate(scenes):
            scene_drawer = SceneDrawer(my_scene)
            scene_drawer.assign_image_location(index)
            scene_drawer.assign_positions()
            scene_drawer.draw()
        return scenes

    @staticmethod
    def save_pickle(scene_list):
        filename = SceneDrawer.pickle_path_format.format(SceneDrawer.pickle_folder, SceneDrawer.pickle_filename)
        with open(filename, "wb") as pickle_file:
            pickle.dump(scene_list, pickle_file)

    @staticmethod
    def load_pickle():
        filename = SceneDrawer.pickle_path_format.format(SceneDrawer.pickle_folder, SceneDrawer.pickle_filename)
        with open(filename, "rb") as pickle_file:
            return pickle.load(pickle_file)


def main():
    SceneDrawer.orchestrate()
    scene_list = SceneDrawer.load_pickle()
    for scene in scene_list:
        print(scene)


if __name__ == "__main__":
    main()
