#import re
#import exrex
import main
import random
from main import list_scenes
from main import objects
from main import Scene


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


def transform(scene, list_indexes):
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


def generate_location_expr(scene, shapedict, templatedict, attribute_indexes):

    location_expression_list = []
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
    from_relative_tuple = ()
    absolute_tuple = () 
    middle_tuple = ()
    relative_tuple = ()
    
    choices[2] = "left to"
    choices[1] = "leftmost"
    choices[0] = "from left"


    if choices[0] == "from left" or choices[0] == "from right":

        target_choice = random_choice(attribute_indexes)
        index = -1
        target_matrix = transform(scene, attribute_indexes[target_choice])

        for i in range(1, 5):
            from_relative_output = from_relative(target_matrix, choices[0], i) #what is number?

            if len(from_relative_output) > 0:
                index = i
                break

        if index != -1:
            from_relative_tuple = generate_from_relative_expr(scene, list(from_relative_output), target_choice, choices[0], index)
       
    if choices[1] == "rightmost" or choices[1] == "leftmost" or choices[1] == "topmost" or choices[1] == "bottommost":

        key_choice = random_choice(attribute_indexes)

        matrix = transform(scene, attribute_indexes[key_choice])
        
        from_absolute = absolute(matrix, choices[1])

        absolute_tuple = generate_absolute_expr(scene, list(matrix), key_choice, choices[1])

    elif choices[1] == "mid":

        target_choice = random_choice(attribute_indexes)
        relative_choice = random_choice(attribute_indexes)

        target_matrix = transform(scene, attribute_indexes[target_choice])
        relative_matrix = transform(scene, attribute_indexes[relative_choice])

        middle(target_matrix, relative_matrix)

        middle_tuple = generate_middle_expr(scene, list(target_matrix), list(relative_matrix), target_choice, relative_choice, choices[1])

    if choices[2] == "left to" or choices[2] == "right to" or choices[2] == "top to" or choices[2] == "bottom to" or choices[2] == "top-left to" or choices[2] == "top-right to" or choices[2] == "bottom-left to" or choices[2] == "bottom-right to":

        target_choice = random_choice(attribute_indexes)
        relative_choice = random_choice(attribute_indexes)

        target_matrix = transform(scene, attribute_indexes[target_choice])
        relative_matrix = transform(scene, attribute_indexes[relative_choice])

        relative_output = relative(target_matrix, relative_matrix, choices[2])

        relative_tuple = generate_relative_expr(scene, list(target_matrix), list(relative_matrix), target_choice, relative_choice, choices[2])


    return [from_relative_tuple, absolute_tuple, middle_tuple, relative_tuple]

    
def generate_from_relative_expr(scene, from_relative_output, target_choice, expression_connector, index):

    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4][0] == from_relative_output[0][0] and obj[4][1] == from_relative_output[0][1]:
            index_list.append(obj[0])

    if index == 1:
        expression += "first "
    elif index == 2:
        expression += "second "
    elif index == 3:
        expression += "third "
    else:
        expression += "forth "
    
    expression += target_choice + " object " + expression_connector

    if expression_connector == "from left":
        expression_tuple.append(expression)
        expression_tuple.append('x from left template')
        expression_tuple.append(tuple(index_list))
    else:
        expression_tuple.append(expression)
        expression_tuple.append('x from right template')
        expression_tuple.append(tuple(index_list))

    return tuple(expression_tuple)

def generate_absolute_expr(scene, absolute_output, key_choice, expression_connector):

    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4][0] == absolute_output[0][0] and obj[4][1] == absolute_output[0][1]:
            index_list.append(obj[0])
    
    expression += expression_connector + " " + key_choice + " object"

    if expression_connector == "leftmost":
        expression_tuple.append(expression)
        expression_tuple.append('leftmost x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "topmost":
        expression_tuple.append(expression)
        expression_tuple.append('topmost x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "bottommost":
        expression_tuple.append(expression)
        expression_tuple.append('bottommost x template')
        expression_tuple.append(tuple(index_list))

    else:
        expression_tuple.append(expression)
        expression_tuple.append('rightmost x template')
        expression_tuple.append(tuple(index_list))

    return tuple(expression_tuple)

def generate_middle_expr(scene, target_matrix, relative_matrix, target_choice, relative_choice, expression_connector):
    
    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4][0] == target_matrix[0][0] and obj[4][1] == target_matrix[0][1]:
            index_list.append(obj[0])

    for obj in scene.objects_tuples:
        if obj[4][0] == relative_matrix[0][0] and obj[4][1] == relative_matrix[0][1]:
            index_list.append(obj[0])

    expression += expression_connector + " " + target_choice + " object"

    expression_tuple.append(expression)
    expression_tuple.append('mid template')
    expression_tuple.append(tuple(index_list))

    return tuple(expression_tuple)

def generate_relative_expr(scene, target_matrix, relative_matrix, target_choice, relative_choice, expression_connector):
    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4][0] == target_matrix[0][0] and obj[4][1] == target_matrix[0][1]:
            index_list.append(obj[0])

    for obj in scene.objects_tuples:
        if obj[4][0] == relative_matrix[0][0] and obj[4][1] == relative_matrix[0][1]:
            index_list.append(obj[0])
    
    expression += target_choice + " object " + expression_connector + " " + relative_choice + " object"

    if expression_connector == "left to":
        expression_tuple.append(expression)
        expression_tuple.append('left to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "right to":
        expression_tuple.append(expression)
        expression_tuple.append('right to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "top to":
        expression_tuple.append(expression)
        expression_tuple.append('top to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "bottom to":
        expression_tuple.append(expression)
        expression_tuple.append('bottom to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "top-left to":
        expression_tuple.append(expression)
        expression_tuple.append('top-left to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "top-right to":
        expression_tuple.append(expression)
        expression_tuple.append('top-right to x template')
        expression_tuple.append(tuple(index_list))

    elif expression_connector == "bottom-left to":
        expression_tuple.append(expression)
        expression_tuple.append('bottom-left to template')
        expression_tuple.append(tuple(index_list))
    
    else:
        expression_tuple.append(expression)
        expression_tuple.append('bottom-right to template')
        expression_tuple.append(tuple(index_list))

    return tuple(expression_tuple)



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

def from_relative(targetMatrix, relativeDirection, number):
    grid_length = 3
    outputset = set()

    targetcolumns = list()
    targetcolumns.append(list())
    targetcolumns.append(list())
    targetcolumns.append(list())

    for coordx, coordy in targetMatrix:
        targetcolumns[coordx].append((coordx, coordy))

    iter_range = list()
    if relativeDirection == 'from left':
        iter_range = range(0,3)
    else:
        iter_range = reversed(range(0,3))

    targetObject = None

    for i in iter_range:
        number -= len(targetcolumns[i])
        if number == 0 and len(targetcolumns[i]) == 1:
            targetObject = targetcolumns[i][0]
            break
        elif number < 0:
            break

    if targetObject is not None:
        outputset.add(targetObject)

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

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = objects("big", "red", "box", (0,0,0))
    object_1.normalized_location = (0,0)
    object_2 = objects("small", "green", "sphere", (2,0,0))
    object_2.normalized_location = (2,0)
    list_object = []
    list_object.append(object_1)
    list_object.append(object_2)

    scene_1 = Scene("", list_object)

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


            info = [index, item.color, item.shape, item.size, item.normalized_location]

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
        
        location_expressions = generate_location_expr(scene_ob, shapedict, templatedict, attribute_indexes)
        scene_ob.list_expressions = expressionlist #set the attribute in the scene object


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



if __name__ == "__main__":
    main()
