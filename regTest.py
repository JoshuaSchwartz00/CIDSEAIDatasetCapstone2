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
                totals["red"].append(index)
            if item.color == "green":
                totals["green"].append(index)
            if item.size == "small":
                totals["small"].append(index)
            if item.size == "large":
                totals["large"].append(index)
            if item.shape == "sphere":
                totals["sphere"].append(index)
            if item.shape == "cube":
                totals["cube"].append(index)
            
            

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