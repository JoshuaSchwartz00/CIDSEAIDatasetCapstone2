from model_drawer import ModelDrawer
from vpython import canvas, scene, vector
from data import Scene, Model
from shutil import move
import itertools
import random
import pickle
import time
import os


class SceneDrawer:
    models_per_scene = range(2, 5)
    pickle_length = 10

    downloads_template = os.path.join(os.getenv("USERPROFILE"), "Downloads") + "\\{}"
    cwd_template = os.getcwd() + "\\{}"
    download_wait_seconds = 5

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

    def draw_and_capture(self, fixed=False):
        my_canvas = canvas(width=SceneDrawer.vpython_canvas_width, height=SceneDrawer.vpython_canvas_height)
        if fixed:
            self.fix_camera(my_canvas)
        self.draw()
        self.capture(my_canvas)
        my_canvas.delete()

    def draw(self):
        for model in self.scene.model_list:
            model_drawer = ModelDrawer(model)
            model_drawer.draw()

    def capture(self, my_canvas):
        image_name = SceneDrawer.filename_from_path(self.scene.image_location)
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
    def orchestrate_pickle():
        SceneDrawer.generate_pickle()

    @staticmethod
    def orchestrate_images():
        scene_list = SceneDrawer.load_pickle()
        SceneDrawer.generate_images(scene_list)
        time.sleep(SceneDrawer.download_wait_seconds)
        SceneDrawer.move_images(scene_list)

    @staticmethod
    def generate_pickle():
        scene_list = SceneDrawer.generate_scenes()
        SceneDrawer.ensure_directory_exists(SceneDrawer.pickle_folder)
        SceneDrawer.save_pickle(scene_list)

    @staticmethod
    def generate_images(scene_list):
        for my_scene in scene_list:
            scene_drawer = SceneDrawer(my_scene)
            scene_drawer.draw_and_capture()

    @staticmethod
    def generate_scenes():
        scene.delete()  # delete built-in vpython canvas; we will make our own for each scene
        scenes = SceneDrawer.generate_permutations()
        for index, my_scene in enumerate(scenes):
            scene_drawer = SceneDrawer(my_scene)
            scene_drawer.assign_image_location(index)
            scene_drawer.assign_positions()
        return scenes

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
    def move_images(scene_list):
        time.sleep(SceneDrawer.download_wait_seconds)
        for my_scene in scene_list:
            SceneDrawer.move_image(my_scene)

    @staticmethod
    def move_image(my_scene):
        image_name = SceneDrawer.filename_from_path(my_scene.image_location)
        downloads_image_path = SceneDrawer.downloads_template.format(image_name)
        cwd_image_path = SceneDrawer.cwd_template.format(my_scene.image_location)
        move(downloads_image_path, cwd_image_path)

    @staticmethod
    def ensure_directory_exists(directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)

    @staticmethod
    def filename_from_path(path):
        return path[path.index("\\") + 1:]

    @staticmethod
    def save_pickle(scenes):
        filename = SceneDrawer.pickle_path_format.format(SceneDrawer.pickle_folder, SceneDrawer.pickle_filename)
        with open(filename, "wb") as pickle_file:
            pickle.dump(scenes, pickle_file)

    @staticmethod
    def load_pickle():
        filename = SceneDrawer.pickle_path_format.format(SceneDrawer.pickle_folder, SceneDrawer.pickle_filename)
        with open(filename, "rb") as pickle_file:
            return pickle.load(pickle_file)

    @staticmethod
    def fix_camera(my_canvas):
        my_canvas.up = vector(0, 1, 0)
        my_canvas.camera.axis = vector(0, 0, -6.21472)
        my_canvas.camera.pos = vector(0, 0, 6.21472)


def generate_image(*, color, shape, size, location, filename, folder):
    SceneDrawer.ensure_directory_exists(folder)  # check directory

    model = Model()  # make model
    model.color = color
    model.shape = shape
    model.size = size
    model.vpython_location = location

    my_scene = Scene()  # make scene
    my_scene.image_location = "{}\\{}.png".format(folder, filename)
    my_scene.model_list = [model]

    scene_drawer = SceneDrawer(my_scene)  # make scene drawer and draw
    scene_drawer.draw_and_capture(fixed=True)
    time.sleep(1)  # wait before moving

    SceneDrawer.move_image(my_scene)


def main():
    SceneDrawer.orchestrate_images()


if __name__ == "__main__":
    main()
