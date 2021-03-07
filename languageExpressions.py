#import re
#import exrex
import main
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

    if attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "green cubes"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["box"])

    if attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "red spheres"
            shapedict.value = list(attribute_indexes["red"] & attribute_indexes["sphere"])

    if attribute_indexes["green"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "green spheres"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["sphere"])

    #color size template
    if attribute_indexes["small"] and attribute_indexes["red"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"]):
            shapedict.key = "small red objects"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"])

    if attribute_indexes["big"] and attribute_indexes["red"]:
        if list(attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "big red objects"
            shapedict.value = list(attribute_indexes["green"] & attribute_indexes["box"])

    if attribute_indexes["small"] and attribute_indexes["green"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"]):
            shapedict.key = "small green objects"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"])

    if attribute_indexes["big"] and attribute_indexes["green"]:
        if list(attribute_indexes["big"] & attribute_indexes["green"]):
            shapedict.key = "big green objects"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"])

    #size shape template
    if attribute_indexes["small"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["box"]):
            shapedict.key = "small cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["box"])

    if attribute_indexes["big"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["box"]):
            shapedict.key = "big cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["box"])

    if attribute_indexes["small"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["sphere"]):
            shapedict.key = "small spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["sphere"])

    if attribute_indexes["big"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["big"] & attribute_indexes["sphere"]):
            shapedict.key = "big spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["sphere"])

    #size color shape template

    if attribute_indexes["small"] and attribute_indexes["red"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["box"]):
            shapedict.key = "small red cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["box"])

    if attribute_indexes["big"] and attribute_indexes["red"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["box"]):
            shapedict.key = "big red cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["box"])

    if attribute_indexes["small"] and attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "small green cubes"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["box"])

    if attribute_indexes["big"] and attribute_indexes["green"] and attribute_indexes["box"]:
        if list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["box"]):
            shapedict.key = "big green cubes"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["box"])

    if attribute_indexes["big"] and attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "big red spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["red"] & attribute_indexes["sphere"])

    if attribute_indexes["small"] and attribute_indexes["red"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["sphere"]):
            shapedict.key = "small red spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["red"] & attribute_indexes["sphere"])

    if attribute_indexes["big"] and attribute_indexes["green"] and attribute_indexes["sphere"]:
        if  list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "big green spheres"
            shapedict.value = list(attribute_indexes["big"] & attribute_indexes["green"] & attribute_indexes["sphere"])

    if attribute_indexes["small"] and attribute_indexes["green"] and attribute_indexes["sphere"]:
        if list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["sphere"]):
            shapedict.key = "small green spheres"
            shapedict.value = list(attribute_indexes["small"] & attribute_indexes["green"] & attribute_indexes["sphere"])
         
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
            info = [index, item.color, item.shape, item.size]
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