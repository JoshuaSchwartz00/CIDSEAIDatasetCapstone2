from languageExpressions import language_controller
from createjson import createjsonfile
from scene_drawer import SceneDrawer
from segment import segment_images


if __name__ == "__main__":
    # img folder for image generation
    scene_list = SceneDrawer.load_pickle()[500:510]
    language_controller(scene_list)
    # results folder for segemented images
    segment_images("segmented_img", scene_list)
    createjsonfile("segmented_img", scene_list, "output.json")
