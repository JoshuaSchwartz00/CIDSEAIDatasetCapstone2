#import re
#import exrex
import main
import random
from main import list_scenes
from main import objects
from main import scene



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


def transform(list_indexes):
    new_set = set()

    for i in list_indexes:
        for obj in scene.objects_tuples:
            if i == obj[0]:
                new_set.add((obj[4][0], obj[4][1])) #info = [index, item.color, item.shape, item.size, item.location]

    return new_set

def random_choice(attribute_indexes):

    local_keys = list(attribute_indexes.keys())
    key_choice = ""

    found = False
    while found == False:
        key_choice = random.choices(local_keys)

        if key_choice[0] in attribute_indexes:
            found = True
        else:
            local_keys.remove(key_choice[0])
        
    return key_choice[0]


def generate_location_expr(shapedict, templatedict, attribute_indexes, scene):


    list1 = ["from left", "from right"]
    list2 = ["leftmost", "rightmost", "mid", "topmost", "bottommost"]
    list3 = ["right to", "left to", "top to", "bottom to", "top-left to", "top-right to", "bottom-left to", "bottom-right to"]

    choices = []
    choices.append(random.choice(list1))
    choices.append(random.choice(list2))
    choices.append(random.choice(list3))
    key_choice = ""
    from_relative_output = ""
    from_absolute_output = ""
    relative_output = ""
    mid_output = ""
    
    choices[2] = "left to"
    choices[1] = "mid"
    choices[0] = "from left"


    if choices[0] == "from left" or choices[0] == "from right":

        target_choice = random_choice(attribute_indexes)
        relative_choice = random_choice(attribute_indexes)

        target_matrix = transform(attribute_indexes[target_choice])
        relative_matrix = transform(attribute_indexes[relative_choice])

        print(target_matrix, relative_matrix)
        for i in range(1, 5):
            from_relative_output = from_relative(target_matrix, relative_matrix, choices[0], i) #what is number?

            if len(from_relative_output) > 0:
                break
        print(from_relative_output, len(from_relative_output))

    if choices[1] == "rightmost" or choices[1] == "leftmost" or choices[1] == "topmost" or choices[1] == "bottommost":

        key_choice = random_choice(attribute_indexes)

        matrix = transform(attribute_indexes[key_choice])
        
        from_absolute = absolute(matrix, choices[1])

    elif choices[1] == "mid":

        target_choice = random_choice(attribute_indexes)
        relative_choice = random_choice(attribute_indexes)

        target_matrix = transform(attribute_indexes[target_choice])
        relative_matrix = transform(attribute_indexes[relative_choice])

        middle(target_matrix, relative_matrix)

    if choices[2] == "left to" or choices[2] == "right to" or choices[2] == "top to" or choices[2] == "bottom to" or choices[2] == "top-left to" or choices[2] == "top-right to" or choices[2] == "bottom-left to" or choices[2] == "bottom-right to":

        target_choice = random_choice(attribute_indexes)
        relative_choice = random_choice(attribute_indexes)

        target_matrix = transform(attribute_indexes[target_choice])
        relative_matrix = transform(attribute_indexes[relative_choice])

        relative_output = relative(target_matrix, relative_matrix, choices[2])


    return [from_relative_output, from_absolute_output, relative_output, mid_output]

    


#matrix define as set of tuple(x-cord, y-cord)

def relative(targetMatrix, relativeMatrix, relativeDirection): #left to/right to

    grid_length = 3
    constraints = list()
    for coordx, coordy in relativeMatrix:
        if relativeDirection == 'left to':
            constraints.append((0, coordx, 0, grid_length))
        elif relativeDirection == 'right to':
            constraints.append((coordx+1,grid_length,0,grid_length))
        elif relativeDirection == 'top to':
            constraints.append((0,grid_length,0,coordy))
        elif relativeDirection == 'bottom to':
            constraints.append((0,grid_length,coordy+1,grid_length))
        elif relativeDirection == 'top-left to':
            constraints.append((0,coordx,0,coordy))
        elif relativeDirection == 'top-right to':
            constraints.append((coordx+1,grid_length,0,coordy))
        elif relativeDirection == 'bottom-left to':
            constraints.append((0,coordx,coordy+1,grid_length))
        elif relativeDirection == 'bottom-right to':
            constraints.append((coordx+1,grid_length,coordy+1,grid_length))

    outputset = set()
    for x_low, x_high, y_low, y_high in constraints:
        for x_cord in range(x_low, x_high):
            for y_cord in range(y_low,y_high):
                if (x_cord, y_cord) in targetMatrix:
                    outputset.add((x_cord, y_cord))

    return outputset

def middle(targetMatrix, relativeMatrix):
    outputset = set()
    for x_coord, y_coord in targetMatrix:
        horizontalcheck = ((x_coord-1,y_coord) in relativeMatrix and (x_coord+1,y_coord) in relativeMatrix)
        verticalcheck = ((x_coord,y_coord-1) in relativeMatrix and (x_coord,y_coord+1) in relativeMatrix)
        if horizontalcheck or verticalcheck:
            outputset.add(x_coord,y_coord)
    return outputset

def absolute(targetMatrix, absoluteDirection):

    grid_length = 3
    constraint = None
    if absoluteDirection == 'leftmost':
        constraint = (0,1,0,grid_length)
    elif absoluteDirection == 'rightmost':
        constraint = (grid_length-1,grid_length,0,grid_length)
    elif absoluteDirection == 'topmost':
        constraint = (0,grid_length,0,1)
    elif absoluteDirection == 'bottommost':
        constraint = (0,grid_length,grid_length-1,grid_length)

    found = False
    repeat = False
    coordinate = None
    for x in range(constraint[0], constraint[1]):
        for y in range(constraint[2], constraint[3]):
            if (x,y) in targetMatrix:
                coordinate = (x,y)
                if not found:
                    found = True
                else:
                    repeat = True
    if not found or repeat:
        return None
    else:
        return coordinate

def from_relative(targetMatrix, relativeMatrix, relativeDirection, number):
    grid_length = 3
    outputset = set()

    targetcolumns = list()
    targetcolumns.append(list())
    targetcolumns.append(list())
    targetcolumns.append(list())

    for coordx, coordy in targetMatrix:
        targetcolumns.append((coordx, coordy))

    relativeColumnsExist = list()
    relativeColumnsExist.append(False)
    relativeColumnsExist.append(False)
    relativeColumnsExist.append(False)

    for coordx, coordy in relativeMatrix:
        relativeColumnsExist[coordx] = True
    print(relativeColumnsExist)
    for exist,idx in enumerate(relativeColumnsExist):
        if exist:
            iter_range = list()
            if relativeDirection == 'from left':
                iter_range = reversed(range(0, idx))
            else:
                iter_range = range(idx+1, grid_length)

            loc_counter = number
            targetObject = None
            for i in iter_range:
                loc_counter = loc_counter - len(targetcolumns[i])
                print(loc_counter)
                print(len(targetcolumns[i]))
                if loc_counter == 0 and len(targetcolumns[i]) == 1:
                    targetObject = targetcolumns[i][0]
                    break
                elif loc_counter < 0:
                    break

            if targetObject is not None:
                outputset.add(targetObject)
    print(outputset)
    return outputset

#generate a list of tuples for each expression: (referring expression, template, (1,3 if it applies to objects 1 and 3))
def generate_tuples(shapedict, templatedict):

    tuple_list = []

    for key in shapedict:
        tuple_list.append((key,templatedict[key], tuple(shapedict[key])))

    return tuple_list

#generate a dictionary of expression templates that our referring expressions use
def generate_templates(shapedict):

    templatedict = {}

    #"<col> object template"
    if "red objects" in shapedict:
        templatedict["red objects"] = "<col> object template"
    if shapedict["green objects"]:
        templatedict["green objects"] = "<col> object template"

    #"<size> object template"
    if "big objects" in shapedict:
        templatedict["big objects"]= "<size> object template"
    if "small objects" in shapedict:
        templatedict["small objects"] = "<size> object template"

    #"<shape> template"
    if "cubes" in shapedict:
        templatedict["cubes"]= "<shape> template"

    if "spheres" in shapedict:
        templatedict["spheres"] = "<shape> template"

    #"<col> <shape> template"
    if "red cubes" in shapedict:
        templatedict["red cubes"] = "<col> <shape> template"
    if "green cubes" in shapedict:
        templatedict["green cubes"]= "<col> <shape> template"
    if "red spheres" in shapedict:
        templatedict["red spheres"] = "<col> <shape> template"
    if "green spheres" in shapedict:
        templatedict["green spheres"] = "<col> <shape> template"

    #"<size> <col> object template"
    if "small red objects" in shapedict:
        templatedict["small red objects"] = "<size> <col> object template"
    if "big red objects" in shapedict:
        templatedict["big red objects"] = "<size> <col> object template"
    if "small green objects" in shapedict:
        templatedict["small green objects"] = "<size> <col> object template"
    if "big green objects" in shapedict:
        templatedict["big green objects"] = "<size> <col> object template"

    
    #"<size> <shape> object template"
    if "small cubes" in shapedict:
        templatedict["small cubes"] = "<size> <shape> object template"
    if "big cubes" in shapedict:
        templatedict["big cubes"] = "<size> <shape> object template"
    if "small spheres" in shapedict:
        templatedict["small spheres"] = "<size> <shape> object template"
    if "big spheres" in shapedict:
        templatedict["big spheres"] = "<size> <shape> object template"

    #"<size> <color> <shape> template"
    if "small red cubes" in shapedict:
        templatedict["small red cubes"] = "<size> <color> <shape> template"
    if "big red cubes" in shapedict:
        templatedict["big red cubes"] = "<size> <color> <shape> template"
    if "small green cubes" in shapedict:
        templatedict["small green cubes"] = "<size> <color> <shape> template"
    if "big green cubes" in shapedict:
        templatedict["big green cubes"] = "<size> <color> <shape> template"
    if "big red spheres" in shapedict:
        templatedict["big red spheres"] = "<size> <color> <shape> template"
    if "small red spheres" in shapedict:
        templatedict["small red spheres"] = "<size> <color> <shape> template"
    if "big green spheres" in shapedict:
        templatedict["big green spheres"] = "<size> <color> <shape> template"
    if "small green spheres" in shapedict:
        templatedict["small green spheres"] = "<size> <color> <shape> template"

    return templatedict
    

#generate referring expressions based on the objects in attribute indexes
def generate_expressions(attribute_indexes):
    
    shapedict = {}
    
    #have to add template dictionary
    #object template
    if "red" in attribute_indexes:
        shapedict["red objects"] = attribute_indexes["red"]
    if "green" in attribute_indexes:
        shapedict["green objects"] = attribute_indexes["green"]
    if "box" in attribute_indexes:
        shapedict["cubes"] = attribute_indexes["box"]
    if "box" in attribute_indexes:
        shapedict["spheres"] = attribute_indexes["sphere"]
    if "big" in attribute_indexes:
        shapedict["big objects"] = attribute_indexes["big"]
    if "small" in attribute_indexes:
        shapedict["small objects"] = attribute_indexes["small"]

    #color shape template
    if "red" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["red"]) & set(attribute_indexes["box"])):
            shapedict["red cubes"] = list(set(attribute_indexes["red"]) & set(attribute_indexes["box"]))


    if "green" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["green"]) & set(attribute_indexes["box"])):
            shapedict["green cubes"] = list(set(attribute_indexes["green"]) & set(attribute_indexes["box"]))

    if "red" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["red"]) & set(attribute_indexes["sphere"])):
            shapedict["red spheres"] = list(set(attribute_indexes["red"]) & set(attribute_indexes["sphere"]))

    if "green" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["green"]) & set(attribute_indexes["sphere"])):
            shapedict["green spheres"] = list(set(attribute_indexes["red"]) & set(attribute_indexes["sphere"]))

    #color size template
    if "small" in attribute_indexes and "red" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["red"])):
            shapedict["small red objects"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["red"]))

    if "big" in attribute_indexes and "red" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["red"])):
            shapedict["big red objects"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["red"]))

    if "small" in attribute_indexes and "green" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["green"])):
            shapedict["small green objects"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["green"]))


    if "big" in attribute_indexes and "green" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["green"])):
            shapedict["big green objects"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["green"]))

    #size shape template
    if "small" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["box"])):
            shapedict["small cubes"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["box"]))

    if "big" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["box"])):
            shapedict["big cubes"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["box"]))

    if "small" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["sphere"])):
            shapedict["small spheres"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["sphere"]))

    if "big" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["sphere"])):
            shapedict["big spheres"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["sphere"]))

    #size color shape template

    if "small" in attribute_indexes and "red" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["red"]) & set(attribute_indexes["box"])):
            shapedict["small red cubes"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["red"]) & set(attribute_indexes["box"]))

    if "big" in attribute_indexes and "red" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["red"]) & set(attribute_indexes["box"])):
            shapedict["big red cubes"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["red"]) & set(attribute_indexes["box"]))

    if "small" in attribute_indexes and "green" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["green"]) & set(attribute_indexes["box"])):
            shapedict["small green cubes"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["green"]) & set(attribute_indexes["box"]))

    if "big" in attribute_indexes and "green" in attribute_indexes and "box" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["green"]) & set(attribute_indexes["box"])):
            shapedict["big green cubes"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["green"]) & set(attribute_indexes["box"]))

    if "big" in attribute_indexes and "red" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["big"]) & set(attribute_indexes["red"]) & set(attribute_indexes["sphere"])):
            shapedict["big red spheres"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["red"]) & set(attribute_indexes["sphere"]))

    if "small" in attribute_indexes and "red" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["red"]) & set(attribute_indexes["sphere"])):
            shapedict["small red spheres"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["red"]) & set(attribute_indexes["sphere"]))

    if "big" in attribute_indexes and "green" in attribute_indexes and "sphere" in attribute_indexes:
        if  list(set(attribute_indexes["big"]) & set(attribute_indexes["green"]) & set(attribute_indexes["sphere"])):
            shapedict["big green spheres"] = list(set(attribute_indexes["big"]) & set(attribute_indexes["green"]) & set(attribute_indexes["sphere"]))

    if "small" in attribute_indexes and "green" in attribute_indexes and "sphere" in attribute_indexes:
        if list(set(attribute_indexes["small"]) & set(attribute_indexes["green"]) & set(attribute_indexes["sphere"])):
            shapedict["small green spheres"] = list(set(attribute_indexes["small"]) & set(attribute_indexes["green"]) & set(attribute_indexes["sphere"]))
         
    return shapedict


def main():

    list_scenes = list()

    object_1 = objects("big", "red", "box", (0,0,0))
    object_2 = objects("small", "green", "sphere", (2,0,0))
    list_object = []
    list_object.append(object_1)
    list_object.append(object_2)

    scene_1 = scene("", list_object)

    list_scenes.append(scene_1)

    for scene_ob in list_scenes:
        attribute_indexes = { #when an object has one of these attributes, add its index to the list for that attribute
            "red" : [],
            "green" : [],
            "small" : [],
            "big" : [],
            "sphere" : [],
            "box" : []
        }

        for index, item in enumerate(scene_ob.list_objects): #make tuple/list for each object like: (1, red, box, small) 
            #(index, color, shape, size)


            info = [index, item.color, item.shape, item.size, item.location]

            scene_ob.objects_tuples.append(info)

            if item.color == "red":
                attribute_indexes["red"].append(index)
            if item.color == "green":
                attribute_indexes["green"].append(index)
            if item.size == "small":
                attribute_indexes["small"].append(index)
            if item.size == "big":
                attribute_indexes["big"].append(index)
            if item.shape == "sphere":
                attribute_indexes["sphere"].append(index)
            if item.shape == "box":
                attribute_indexes["box"].append(index)
        
        #collect the data
        shapedict = generate_expressions(attribute_indexes)
        templatedict = generate_templates(shapedict)
        expressionlist = generate_tuples(shapedict, templatedict)
        scene.list_expressions = expressionlist #set the attribute in the scene object
        location_expressions = generate_location_expr(shapedict, templatedict, attribute_indexes, scene)

        print("SHAPEDICT: ")
        print(shapedict)
        print()
        print("TEMPLATE DICT: ")
        print(templatedict)
        print()
        print("EXPRESSION LIST: ")
        print(expressionlist)
        print()
        print("LOCATION EXPRESSIONS: ")
        print(location_expressions)

        return expressionlist


if __name__ == "__main__":
    main()
