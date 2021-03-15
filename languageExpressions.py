#import re
#import exrex
import main
import random
from main import list_scenes


    #print(exrex.generate('This is (a (code|cake|test)|an (apple|elf|output))\.'))
    #print("\n".join(exrex.generate('This is (a (color|cake|test)|an (apple|elf|output))\.')))
    #print("\n".join(exrex.generate('(small|large) (red|green) (cube|sphere)')))

# class object: 
#     size = ""
#     color = ""
#     shape = ""
#     x = 0 #need to compare x coord for left/right
#     y = 0
#     z = 0
#     def __init__(self, size, color, shape):
#         self.size = size
#         self.color = color
#         self.shape = shape

# shapedict = {
#                 f"{shape.size} objects" : "<size> object template",
#                 f"{shape.color} objects" : "<col> object template",
#                 f"{shape.shape}s" : "<shape> template",
#                 f"{shape.color} {shape.shape}s" : "<col> <shape> template",
#                 f"{shape.size} {shape.color} objects" : "<size> <col> object template",
#                 f"{shape.size} {shape.shape}s" : "<size> <shape> object template",
#                 f"{shape.size} {shape.color} {shape.shape}s" : "<size> <color> <shape> template",
#             }
 
#scene.list_expressions.update(shapedict)

def generate_location_expr(shapedict, templatedict, attribute_indexes, scene):

    list1 = ["from left", "from right"]
    list2 = ["leftmost", "rightmost", "mid"]
    list3 = ["right to", "left to"]

    choices = []
    choices.append(random.choice(list1))
    choices.append(random.choice(list2))
    choices.append(random.choice(list3))

    if choices[1] == "rightmost" or choices[1] == "leftmost":
        duplicate = True
        while(duplicate == True):

            duplicate = False
            ran_key = random.choice(shapedict.keys)

            list_indexes = shapedict[ran_key]
            dict_objects = dict()

            for i in list_indexes:
                for obj in scenes.object_tuples:
                    if i in obj:
                        dict_object[i] = obj[4]

            if choices[1] == "leftmost":
                leftmost_index = None
        

                for i in list_indexes:

                    if leftmost_index == None:
                        leftmost_index = i
                    elif dict_object[leftmost_index][0] > dict_object[i][0]:
                        leftmost_index = i
                        duplicate = False
                    elif dict_object[leftmost_index][0] == dict_object[i][0]:
                        duplicate = True


            else if choices[1] == "rightmost":
                rightmost_index = None
                duplicate = False

                for i in list_indexes:

                    if rightmost_index == None:
                        rightmost_index = i
                    elif dict_object[rightmost_index][0] < dict_object[i][0]:
                        rightmost_index = i
                        duplicate = False
                    elif dict_object[rightmost_index][0] == dict_object[i][0]:
                        duplicate = True

    else:



def generate_tuples(shapedict, templatedict):

    tuple_list = []

    for key in shapedict:
        tuple_list.append((key,templatedict[key], tuple(shapedict[key])))

    return tuple_list

def generate_templates(shapedict):

    templatedict = {}

    #"<col> object template"
    if shapedict["red objects"]:
        templatedict.key = "red objects"
        templatedict.value = "<col> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["green objects"]:
        templatedict.key = "green objects"
        templatedict.value = "<col> object template"
        templatedict.add(templatedict.key, templatedict.value)

    #"<size> object template"
    if shapedict["big objects"]:
        templatedict.key = "big objects"
        templatedict.value = "<size> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small objects"]:
        templatedict.key = "small objects"
        templatedict.value = "<size> object template"
        templatedict.add(templatedict.key, templatedict.value)

    #"<shape> template"
    if shapedict["cubes"]:
        templatedict.key = "cubes"
        templatedict.value = "<shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["spheres"]:
        templatedict.key = "spheres"
        templatedict.value = "<shape> template"
        templatedict.add(templatedict.key, templatedict.value)

    #"<col> <shape> template"
    if shapedict["red cubes"]:
        templatedict.key = "red cubes"
        templatedict.value = "<col> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["green cubes"]:
        templatedict.key = "green cubes"
        templatedict.value = "<col> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["red spheres"]:
        templatedict.key = "red spheres"
        templatedict.value = "<col> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["green spheres"]:
        templatedict.key = "green spheres"
        templatedict.value = "<col> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)

    #"<size> <col> object template"
    if shapedict["small red objects"]:
        templatedict.key = "small red objects"
        templatedict.value = "<size> <col> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big red objects"]:
        templatedict.key = "big red objects"
        templatedict.value = "<size> <col> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small green objects"]:
        templatedict.key = "small green objects"
        templatedict.value = "<size> <col> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big green objects"]:
        templatedict.key = "big green objects"
        templatedict.value = "<size> <col> object template"
        templatedict.add(templatedict.key, templatedict.value)
    
    #"<size> <shape> object template"
    if shapedict["small cubes"]:
        templatedict.key = "small cubes"
        templatedict.value = "<size> <shape> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big cubes"]:
        templatedict.key = "big cubes"
        templatedict.value = "<size> <shape> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small spheres"]:
        templatedict.key = "small spheres"
        templatedict.value = "<size> <shape> object template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big spheres"]:
        templatedict.key = "big spheres"
        templatedict.value = "<size> <shape> object template"
        templatedict.add(templatedict.key, templatedict.value)

    #"<size> <color> <shape> template"
    if shapedict["small red cubes"]:
        templatedict.key = "small red cubes"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big red cubes"]:
        templatedict.key = "big red cubes"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small green cubes"]:
        templatedict.key = "small green cubes"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big green cubes"]:
        templatedict.key = "big green cubes"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big red spheres"]:
        templatedict.key = "big red spheres"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small red spheres"]:
        templatedict.key = "small red spheres"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["big green spheres"]:
        templatedict.key = "big green spheres"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)
    if shapedict["small green spheres"]:
        templatedict.key = "small green spheres"
        templatedict.value = "<size> <color> <shape> template"
        templatedict.add(templatedict.key, templatedict.value)

    return templatedict
    


def generate_expressions(attribute_indexes):
    
    shapedict = {}
    
    #have to add template dictionary
    #object template
    if attribute_indexes["red"]:
        shapedict.key = "red objects"
        shapedict.value = attribute_indexes["red"]
        shapedict.add(shapedict.key, shapedict.value)
    if attribute_indexes["green"]:
        shapedict.key = "green objects"
        shapedict.value = attribute_indexes["green"]
        shapedict.add(shapedict.key, shapedict.value)
    if attribute_indexes["box"]:
        shapedict.key = "cubes"
        shapedict.value = attribute_indexes["box"]
        shapedict.add(shapedict.key, shapedict.value)
    if attribute_indexes["sphere"]:
        shapedict.key = "spheres"
        shapedict.value = attribute_indexes["sphere"]
        shapedict.add(shapedict.key, shapedict.value)
    if attribute_indexes["big"]:
        shapedict.key = "big objects"
        shapedict.value = attribute_indexes["big"]
        shapedict.add(shapedict.key, shapedict.value)
    if attribute_indexes["small"]:
        shapedict.key = "small objects"
        shapedict.value = attribute_indexes["small"]
        shapedict.add(shapedict.key, shapedict.value)

    #color shape template
    if attribute_indexes["red"] and attribute_indexes["box"]:
        if list(attribute_indexes["red"] & attribute_indexes["box"]):
            shapedict.key = "red cubes"
            shapedict.value = list(attribute_indexes["red"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)


    if attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "green cubes"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "red spheres"
            shapedict.value = list(attribute_indexes["red"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["green"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "green spheres"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    #color size template
    if attribute_indexes["small"] and attribute_indexes["red"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"]):
            shapedict.key = "small red objects"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["red"]:
        if list(attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "big red objects"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["small"] and attribute_indexes["green"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"]):
            shapedict.key = "small green objects"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["green"]:
        if list(attribute_indexes["big"] & attribute_indexes["green"]):
            shapedict.key = "big green objects"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"])
            shapedict.add(shapedict.key, shapedict.value)

    #size shape template
    if attribute_indexes["small"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["box"]):
            shapedict.key = "small cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["box"]):
            shapedict.key = "big cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["small"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["sphere"]):
            shapedict.key = "small spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["big"] & attribute_indexes["sphere"]):
            shapedict.key = "big spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    #size color shape template

    if attribute_indexes["small"] and attribute_indexes["red"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["box"]):
            shapedict.key = "small red cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["red"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["box"]):
            shapedict.key = "big red cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["small"] and attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "small green cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "big green cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["box"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "big red spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["small"] and attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "small red spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["big"] and attribute_indexes["green"] and attribute_indexes["sphere"]:
        if  list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "big green spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)

    if attribute_indexes["small"] and attribute_indexes["green"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "small green spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["sphere"])
            shapedict.add(shapedict.key, shapedict.value)
         
    return shapedict


def main():
    
    for scene in list_scenes:
        attribute_indexes = { #when an object has one of these attributes, add its index to the list for that attribute
            "red" : [],
            "green" : [],
            "small" : [],
            "big" : [],
            "sphere" : [],
            "box" : []
        }
        for index, item in enumerate(scene.list_objects): #make tuple/list for each object like: (1, red, box, small) 
            #(index, color, shape, size)


            info = [index, item.color, item.shape, item.size, item.location]

            scene.objects_tuples.append(info)

            if item.color == "red":
                attribute_indexes["red"].append(index)
            if item.color == "green":
                attribute_indexes["green"].append(index)
            if item.size == "small":
                attribute_indexes["small"].append(index)
            if item.size == "large":
                attribute_indexes["large"].append(index)
            if item.shape == "sphere":
                attribute_indexes["sphere"].append(index)
            if item.shape == "cube":
                attribute_indexes["cube"].append(index)
                
    
            
            

#          
thisdict = {
"" : "<col> object template",
"" : "<shape> template",
"" : "<col> <shape> template",
"" : "<size> <col> object template",
"" : "<size> <color> <shape> template",
"" : "left to x template",
"" : "x from left template"
}


main()