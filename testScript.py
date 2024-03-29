import os
import time
import json
import glob
from segment import segment_images
import random
from data import Model, Scene
from scene_drawer import generate_image


pixel_map = {(-2, 2, 0): (110, 86), (0, 2, 0): (250, 86), (2, 2, 0): (390, 86),
                (-2, 0, 0): (110, 232), (0, 0, 0): (250, 232), (2, 0, 0): (390, 232),
                (-2, -2, 0): (110, 378), (0, -2, 0): (250, 378), (2, -2, 0): (390, 378)}

#image generation script generates 4000+ images
def test1() -> bool:
    pass
    # image_path_files = glob.glob(os.getcwd() + "\\img\\*.jpg")

    # image_count = len(image_path_files)

    # return image_count > 4000

#makes a segmentation mask
def test2() -> bool:
    list_objects = list()
    
    # a = Model()
    # a.color = "green"
    # a.pixel_location = (250,232)
    # list_objects.append(a)
    # a = Model()
    # a.color = "green"
    # a.pixel_location = (390,378)
    # list_objects.append(a)
    # a = Model()
    # a.color = "red"
    # a.pixel_location = (390,86)
    # list_objects.append(a)
    color_choice = "red"
    shape_choice = "sphere"
    size_choice = "big"
    loc_choice = (-2, -2, 0)
    filename = "scene0"
    folder = "temp"

    a = Model()
    a.color = "red"
    a.size = size_choice
    a.shape = shape_choice
    a.pixel_location = pixel_map[(-2,-2, 0)]
    list_objects.append(a)
    
    generate_image(color=color_choice, shape=shape_choice, size=size_choice, location=loc_choice, filename=filename, folder=folder)

    sc = Scene()
    sc.image_location = "temp/scene0.png"
    sc.model_list = list_objects
    sc.list_expressions = [("objects","template",[0])]
    list_scene = list()
    list_scene.append(sc)
    segment_images("temp_result", list_scene)


#generate image correctly
#VISUAL INSPECTION
def test3() -> bool:
    color_list = ["red", "green"]
    shape_list = ["box", "sphere"]
    size_list = ["big", "small"]
    location_list = [(-2, -2, 0), (-2, 0, 0), (-2, 2, 0), (0, -2, 0), (0, 0, 0), (0, 2, 0), (2, -2, 0), (2, 0, 0), (2, 2, 0)]

    list_ob = []

    path = os.getcwd()

    if(not os.path.exists(os.getcwd() + "\\temp")):
        os.mkdir(os.getcwd() + "\\temp")

    if(not os.path.exists(os.getcwd() + "\\temp_result")):
        os.mkdir(os.getcwd() + "\\temp_result")

    list_scene = []

    for i in range(10):
        color_choice = random.choice(color_list)
        shape_choice = random.choice(shape_list)
        size_choice = random.choice(size_list)
        loc_choice = random.choice(location_list)
        filename = f"scene{i}"
        folder = "temp"

        generate_image(color=color_choice, shape=shape_choice, size=size_choice, location=loc_choice, filename=filename, folder=folder)

        list_objects = list()
        a = Model()
        a.color = color_choice
        a.size = size_choice
        a.shape = shape_choice
        a.pixel_location = pixel_map[loc_choice]
        list_objects.append(a)
        # a = Model()
        # a.color = "green"
        # a.pixel_location = (250,232)
        # list_objects.append(a)
        # a = Model()
        # a.color = "green"
        # a.pixel_location = (390,378)
        # list_objects.append(a)
        # a = Model()
        # a.color = "red"
        # a.pixel_location = (390,86)
        # list_objects.append(a)
        sc = Scene()
        sc.image_location = f"{folder}\\scene{i}.png"
        sc.model_list = list_objects
        sc.list_expressions = [("objects","template",[0])]
        list_scene.append(sc)

    segment_images("temp_result", list_scene)

    #VISUALLY INSPECT THIS SHIT
    

#another visual inspection???
def test4() -> bool:
    color_list = ["red", "green"]
    shape_list = ["box", "sphere"]
    size_list = ["big", "small"]
    location_list = [(-2, -2, 0), (-2, 0, 0), (-2, 2, 0), (0, -2, 0), (0, 0, 0), (0, 2, 0), (2, -2, 0), (2, 0, 0), (2, 2, 0)]

    list_ob = []

    path = os.getcwd()

    if(not os.path.exists(os.getcwd() + "\\temp")):
        os.mkdir(os.getcwd() + "\\temp")

    if(not os.path.exists(os.getcwd() + "\\temp_result")):
        os.mkdir(os.getcwd() + "\\temp_result")

    list_scene = []

    for i in range(10):
        color_choice = random.choice(color_list)
        shape_choice = random.choice(shape_list)
        size_choice = random.choice(size_list)
        loc_choice = random.choice(location_list)
        filename = f"scene{i}"
        folder = "temp"

        generate_image(color=color_choice, shape=shape_choice, size=size_choice, location=loc_choice, filename=filename, folder=folder)

        list_objects = list()
        a = Model()
        a.color = color_choice
        a.size = size_choice
        a.shape = shape_choice
        a.pixel_location = pixel_map[loc_choice]
        list_objects.append(a)
        # a = Model()
        # a.color = "green"
        # a.pixel_location = (250,232)
        # list_objects.append(a)
        # a = Model()
        # a.color = "green"
        # a.pixel_location = (390,378)
        # list_objects.append(a)
        # a = Model()
        # a.color = "red"
        # a.pixel_location = (390,86)
        # list_objects.append(a)
        sc = Scene()
        sc.image_location = f"{folder}\\scene{i}.png"
        sc.model_list = list_objects
        sc.list_expressions = [("objects","template",[])]
        list_scene.append(sc)

    segment_images("temp_result", list_scene)

    #VISUALLY INSPECT THIS SHIT

    #VISUALLY INSPECT THIS SHIT

#
def test5() -> bool:
    pass
    

#checks if the number of segmentation mask images equals the number of language expressions
def test6() -> bool:
    output = json.load("output.json")

    num_output = len(output)

    segmentation_path_files = glob.glob(os.getcwd() + "\\segmented_img\\*.jpg") #seg mask image file

    seg_count = len(segmentation_path_files)

    return num_output == seg_count


if __name__ == "__main__":
    #command = "python main.py"
    #os.system(command)
    test4()
    exit(0)
    #runs all the tests
    if(test1()):
        print("Test 1 passed.")
    else:
        print("Failure occured in Test 1.")
        
    if(test2()):
        print("Test 2 passed.")
    else:
        print("Failure occured in Test 2.")

    if(test3()):
        print("Test 3 passed.")
    else:
        print("Failure occured in Test 3.")
        
    if(test4()):
        print("Test 4 passed.")
    else:
        print("Failure occured in Test 4.")

    if(test5()):
        print("Test 5 passed.")
    else:
        print("Failure occured in Test 5.")
        
    if(test6()):
        print("Test 6 passed.")
    else:
        print("Failure occured in Test 6.")
    
    #lets the program sleep so it gives it time to finish all the functions and image saving
    #time.sleep(60)

    #removes all the unneeded data
    #os.remove("generated.json")
    #os.rmdir("output")