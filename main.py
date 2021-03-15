# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import itertools
import time

from PIL import ImageGrab
from vpython import *
from random import shuffle, randint

list_scenes = list()
scenes_count = 1  # to store the file number
pixelCoorDict = {(-2, 2, 0): (110, 86), (0, 2, 0): (250, 86), (2, 2, 0): (390, 86),
                 (-2, 0, 0): (110, 232), (0, 0, 0): (250, 232), (2, 0, 0): (390, 232),
                 (-2, -2, 0): (110, 378), (0, -2, 0): (250, 378), (2, -2, 0): (390, 378)}

# Press the green button in the gutter to run the script.
class objects:
    size = ""
    color = ""
    shape = ""
    location = (0, 0, 0)

    def __init__(self, size, colors, shape, location): 
        #objects can be: small or big, red or green, box or sphere
        self.size = size
        self.color = colors
        self.shape = shape
        self.location = location  # a tuple (x, y, z)

    def getPixCoordinate(self):
        return pixelCoorDict[self.location]


class scene:
    image_location = ""  # filename
    list_objects = list()
    objects_tuples = list()
    grid = () #(3,3)
    #tuple/list = (ref expr, template, (1,3 if it applies to objects 1 and 3))
    list_expressions = list() #(index, color, shape, size)
    
    #old
    # {c1.size} objects" : ["<size> object template"]
    # {'small objects': '<size> object template', 'red objects': '<col> object template', 'cubes': '<shape> template', 'red cubes': '<col> <shape> template', 'small red objects': '<size> <col> object template', 'small cubes': '<size> <shape> object template', 'small red cubes': '<size> <color> <shape> template'}
    
    
    list_segmented_image = list()  # ((c1.size) objects, <size> object, segmented image path)

    def __init__(self, im_location, list_objects):
        self.image_location = im_location
        self.list_objects = list_objects


def draw_box(position, colors, size):
    length = vector(0, 0, 0)
    if size == "small":
        length = vector(0.7, 0.7, 0.7)
    elif size == "big":
        length = vector(1.2, 1.2, 1.2)
    the_color = color.green
    if colors == "red":
        the_color = color.red
    box(color=the_color, pos=position, size=length).rotate(angle=radians(15), axis=vector(1, 1, 0))


def draw_sphere(position, colors, size):
    radius = 0
    if size == "small":
        radius = 0.4
    elif size == "big":
        radius = 0.8
    the_color = color.green
    if colors == "red":
        the_color = color.red
    sphere(color=the_color, pos=position, radius=radius)

def isOverlap(object_list, obj):
    (colors, size, shape, pos) = obj
    for obj_t in object_list:
        (colors1, size1, shape1, pos1) = obj_t
        if pos1 == pos:
            return True
        if colors == colors and size == size1 and shape == shape1:
            return True
    return False
    

def draw_objects(obj_in_the_sence, list_object):
    this_obj = permutation_list[randint(0, len(permutation_list) - 1)]

    while isOverlap(obj_in_the_sence, this_obj):
        this_obj = permutation_list[randint(0, len(permutation_list) - 1)]

    (colors, size, shape, pos) = this_obj
    obj_in_the_sence.append(this_obj)
    (pos_x, pos_y, pos_z) = pos
    object_1 = objects(size=size, location=pos, shape=shape, colors=colors)
    # To store the object in a list
    list_object.append(object_1)
    # Draw shapes
    if shape == "box":
        draw_box(position=vector(pos_x, pos_y, pos_z), colors=colors, size=size)
    else:
        draw_sphere(position=vector(pos_x, pos_y, pos_z), colors=colors, size=size)
    return obj_in_the_sence, list_object


def capture_image(list_object, sence):
    # =====  capture the Scenes =====
    global scenes_count
    time.sleep(0.15)
    im = ImageGrab.grab((8, 95, 505, 570))
    filename = "img\\object{num}.jpg".format(num=scenes_count)
    scenes_count += 1
    im.save(filename)
    # storing data to objects
    scene_obj = scene(filename, list_object)
    list_scenes.append(scene_obj)
    # reset the canvas
    canvas.delete(self=sence)


if __name__ == '__main__':
    # =====  Generating permutation list  =====
    all_list = [["red", "green"], ["big", "small"], ["box", "sphere"],
                [(-2, -2, 0), (-2, 0, 0), (-2, 2, 0), (0, -2, 0), (0, 0, 0), (0, 2, 0), (2, -2, 0), (2, 0, 0), (2, 2, 0)]]
    permutation_list = list(itertools.product(*all_list))
    shuffle(permutation_list)  # To shuffle the list
    
# ===== Make scenes of objects  =====
    for idx1 in range(0, (8*8*8*8+8*8*8+8*8)):
        sence = canvas(width=500, height=500)
        list_object = list()
        obj_in_the_sence = list()
        (obj_in_the_sence, list_object) = draw_objects(obj_in_the_sence, list_object)
        (obj_in_the_sence, list_object) = draw_objects(obj_in_the_sence, list_object)
        if idx1 >= 64:
            (obj_in_the_sence, list_object) = draw_objects(obj_in_the_sence, list_object)
        if idx1 >= 576:
            (obj_in_the_sence, list_object) = draw_objects(obj_in_the_sence, list_object)
        capture_image(list_object, sence)


    # # ===== To print the objects in each scenes =====
    # for sence in list_scenes:
    #     print(sence.image_location)
    #     for obj in sence.list_objects:
    #         print(obj.size)
    #         print(obj.shape)
    #         print(obj.color)
    #         print(obj.location)

