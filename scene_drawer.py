from model_drawer import ModelDrawer
from vpython import canvas, scene
from data import Scene
import itertools
import random
import pickle
import time
import os


class SceneDrawer:
    models_per_scene = range(2, 5)

    downloads_template = os.path.join(os.getenv("USERPROFILE"), "Downloads") + "\\{image_name}"
    cwd_template = os.getcwd() + "\\{image_location}"
    download_wait_seconds = 1

    image_folder = "img"
    image_filename = "scene"
    image_location_format = "{}\\{}{}.png"

    pickle_folder = "pickle"
    pickle_filename = "scene_list"
    pickle_path_format = "{}\\{}.pickle"

    vpython_canvas_width = 500
    vpython_canvas_height = 500
    vpython_redraw_flag = "redraw"
    vpython_draw_complete_flag = "draw_complete"

    # maps vpython location to pixel location
    pixel_map = {(-2, 2, 0): (110, 86), (0, 2, 0): (250, 86), (2, 2, 0): (390, 86),
                 (-2, 0, 0): (110, 232), (0, 0, 0): (250, 232), (2, 0, 0): (390, 232),
                 (-2, -2, 0): (110, 378), (0, -2, 0): (250, 378), (2, -2, 0): (390, 378)}

    def __init__(self, my_scene):
        self.scene = my_scene

    def __str__(self):
        return str(self.scene)

    def draw(self):
        image_name = SceneDrawer.filename_from_path(self.scene.image_location)
        my_canvas = canvas(width=SceneDrawer.vpython_canvas_width, height=SceneDrawer.vpython_canvas_height)
        for model in self.scene.model_list:
            model_drawer = ModelDrawer(model)
            model_drawer.draw()
        my_canvas.waitfor(SceneDrawer.vpython_redraw_flag)
        my_canvas.waitfor(SceneDrawer.vpython_draw_complete_flag)
        my_canvas.capture(image_name)
        my_canvas.delete()

    def assign_image_location(self, index):
        self.scene.image_location = self.image_location_format.format(SceneDrawer.image_folder,
                                                                      SceneDrawer.image_filename, index)

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
        SceneDrawer.ensure_directory_exists(SceneDrawer.image_folder)
        scene_list = SceneDrawer.generate_scenes()
        SceneDrawer.move_images(scene_list)
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
                my_scene = Scene()
                my_scene.model_list = ModelDrawer.model_tuples_to_models(model_tuples)
                scenes.append(my_scene)
        return scenes

    @staticmethod
    def generate_scenes():
        scene.delete()  # delete built-in vpython canvas; we will make our own for each scene
        scenes = SceneDrawer.generate_permutations()
        for index, my_scene in enumerate(scenes):
            scene_drawer = SceneDrawer(my_scene)
            scene_drawer.assign_image_location(index)
            scene_drawer.assign_positions()
            scene_drawer.draw()
        return scenes

    @staticmethod
    def move_images(scene_list):
        time.sleep(SceneDrawer.download_wait_seconds)
        for my_scene in scene_list:
            SceneDrawer.move_image(my_scene)

    @staticmethod
    def move_image(my_scene):
        image_location = my_scene.image_location
        image_name = SceneDrawer.filename_from_path(image_location)
        downloads_image_path = SceneDrawer.downloads_template.format(image_name=image_name)
        cwd_image_path = SceneDrawer.cwd_template.format(image_location=image_location)
        os.rename(downloads_image_path, cwd_image_path)

    @staticmethod
    def filename_from_path(path):
        return path[path.index("\\") + 1:]

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
    for my_scene in scene_list:
        print(my_scene)


if __name__ == "__main__":
    main()
