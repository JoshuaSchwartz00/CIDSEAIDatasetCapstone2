from languageExpressions import language_controller
from scene_drawer import SceneDrawer
from segment import segment_images
from createjson import createjsonfile
if __name__ == "__main__":
    #img folder for image generation
    scene_list = SceneDrawer.load_pickle()
    for sc in scene_list:
        print(sc)

    language_controller(scene_list)
    #results folder for segemented images
    segment_images("segmented_img", scene_list)
    createjsonfile("segmented_img", scene_list, "output.json")

