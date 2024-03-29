#import re
#import exrex
import random
from data import Model
from data import Scene


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

#returns a set of locations if the index matches
def transform(scene, list_indexes):
    new_set = set()

    for i in list_indexes:
        for obj in scene.objects_tuples:
            if i == obj[0]:
                new_set.add((obj[4][0], obj[4][1])) #info = [index, item.color, item.shape, item.size, item.location]

    return new_set

#chooses a random object to impose a language expression on
def random_choice(attribute_indexes):
    print(attribute_indexes)
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


def valid_attribute_key_filter(attribute_indexes):
    valid_keys = list()

    for key in list(attribute_indexes.keys()):
        if len(attribute_indexes[key]) > 0 :
            valid_keys.append(key)
    return valid_keys

def permute_pair(attribute_indexes):

    valid_keys_pair = list()

    valid_keys = valid_attribute_key_filter(attribute_indexes)
    
    for valid_key in valid_keys:
        for valid_key2 in valid_keys:
            valid_keys_pair.append((valid_key, valid_key2))
    return valid_keys_pair



#generates 3 language expressions per scene, one each for relative, absolute, and middle positions
def generate_location_expr(scene, shapedict, templatedict, attribute_indexes):

    #instantiate expression lists the code is going to pull from
    location_expression_list = []
    list1 = ["from left", "from right"]
    list2 = ["leftmost", "rightmost", "topmost", "bottommost"]
    list3 = ["right to", "left to", "top to", "bottom to", "top-left to", "top-right to", "bottom-left to", "bottom-right to", "middle of"]

    choices = []
    choices.append(random.choice(list1))
    choices.append(random.choice(list2))
    choices.append(random.choice(list3))
    print(choices)
    key_choice = ""
    from_relative_output = ""
    from_absolute_output = ""
    relative_output = ""
    mid_output = ""
    from_relative_tuple = ()
    absolute_tuple = () 
    middle_tuple = ()
    relative_tuple = ()
    
    #hard coded
    #choices[2] = "middle of"
    #choices[1] = "rightmost"
    #choices[0] = "from right"

    #run functions that generate the matrix positions of the output for all types of positional expressions: relative, absolute, and middle

    if choices[0] == "from left" or choices[0] == "from right":

        valid_keys = valid_attribute_key_filter(attribute_indexes)

        found = False
        while(len(valid_keys) > 0 and not found):
            target_key = random.choices(valid_keys)[0]
            valid_keys.remove(target_key)

            # target_choice = attribute_indexes[target_key]
            index = -1
            target_matrix = transform(scene, attribute_indexes[target_key])

            for i in range(1, 5):
                from_relative_output = from_relative(target_matrix, choices[0], i) #what is number?

                if len(from_relative_output) > 0:
                    index = i
                    break

            if index != -1:
                from_relative_tuple = generate_from_relative_expr(scene, list(from_relative_output), target_key, choices[0], index)
                found = True
       
    if choices[1] == "rightmost" or choices[1] == "leftmost" or choices[1] == "topmost" or choices[1] == "bottommost":
        valid_keys = valid_attribute_key_filter(attribute_indexes)

        found = False
        while(len(valid_keys) > 0 and not found):
            target_key = random.choices(valid_keys)[0]
            valid_keys.remove(target_key)

            matrix = transform(scene, attribute_indexes[target_key])
            
            from_absolute = absolute(matrix, choices[1])

            if from_absolute is not None:
                absolute_tuple = generate_absolute_expr(scene, from_absolute, target_key, choices[1])
                found = True

    if choices[2] == "left to" or choices[2] == "right to" or choices[2] == "top to" or choices[2] == "bottom to" or choices[2] == "top-left to" or choices[2] == "top-right to" or choices[2] == "bottom-left to" or choices[2] == "bottom-right to":

        valid_keys_pair = permute_pair(attribute_indexes)

        found = False
        while(len(valid_keys_pair) > 0 and not found):
            keys_pair = random.choices(valid_keys_pair)[0]
            valid_keys_pair.remove(keys_pair)

            target_choice = keys_pair[0]
            relative_choice = keys_pair[1]

            target_matrix = transform(scene, attribute_indexes[target_choice])
            relative_matrix = transform(scene, attribute_indexes[relative_choice])

            relative_output = relative(target_matrix, relative_matrix, choices[2])

            if len(relative_output) > 0:
                relative_tuple = generate_relative_expr(scene, list(relative_output), target_choice, relative_choice, choices[2])
                found = True
    else:
        valid_keys_pair = permute_pair(attribute_indexes)

        found = False
        while(len(valid_keys_pair) > 0 and not found):

            keys_pair = random.choices(valid_keys_pair)[0]
            valid_keys_pair.remove(keys_pair)
            target_choice = keys_pair[0]
            relative_choice = keys_pair[1]

            target_matrix = transform(scene, attribute_indexes[target_choice])
            relative_matrix = transform(scene, attribute_indexes[relative_choice])

            middleset = middle(target_matrix, relative_matrix)

            if len(middleset) > 0:
                relative_tuple = generate_relative_expr(scene, list(middleset),  target_choice, relative_choice, choices[2])
                print(relative_tuple)
                found = True        

    return [from_relative_tuple, absolute_tuple, relative_tuple]

#creates  an expression involving "xth from the..." relative position
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

#creates an expression involving absolute position
def generate_absolute_expr(scene, absolute_output, key_choice, expression_connector):

    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4][0] == absolute_output[0] and obj[4][1] == absolute_output[1]:
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

#creates an expression involving objects in the middle of the image
# def generate_middle_expr(scene, target_output, target_choice, relative_choice, expression_connector):
    
#     expression_tuple = list()
#     index_list = list()
#     expression = ""

#     for obj in scene.objects_tuples:
#         if obj[4] in target_output:
#             index_list.append(obj[0])


#     expression += expression_connector + " " + target_choice + " object"

#     expression_tuple.append(expression)
#     expression_tuple.append('mid template')
#     expression_tuple.append(tuple(index_list))

#     return tuple(expression_tuple)

#creates an expression involving relative position
def generate_relative_expr(scene, target_output,  target_choice, relative_choice, expression_connector):
    expression_tuple = list()
    index_list = list()
    expression = ""

    for obj in scene.objects_tuples:
        if obj[4] in target_output:
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
    
    elif expression_connector == "bottom-right to":
        expression_tuple.append(expression)
        expression_tuple.append('bottom-right to template')
        expression_tuple.append(tuple(index_list))
    else:
        expression_tuple.append(expression)
        expression_tuple.append('middle of template')
        expression_tuple.append(tuple(index_list))
    return tuple(expression_tuple)



#matrix define as set of tuple(x-cord, y-cord)
#sets the relative position according to the image matrix
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

#sets the middle position according to the image matrix
def middle(targetMatrix, relativeMatrix):
    outputset = set()
    for x_coord, y_coord in targetMatrix:
        horizontalcheck = ((x_coord-1,y_coord) in relativeMatrix and (x_coord+1,y_coord) in relativeMatrix)
        verticalcheck = ((x_coord,y_coord-1) in relativeMatrix and (x_coord,y_coord+1) in relativeMatrix)
        if horizontalcheck or verticalcheck:
            outputset.add((x_coord,y_coord))
    return outputset

#sets the absolute position according to the iamge matrix
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

#finds the target object and returns it in an output set
def from_relative(targetMatrix, relativeDirection, number):

    print(targetMatrix)
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
            print(number, targetcolumns[i])
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

    print("shapedict")
    print(shapedict)
    print("templatedict")
    print(templatedict)

    for key in shapedict:
        
        tuple_list.append((key,templatedict[key], tuple(shapedict[key])))

    return tuple_list

#generate a dictionary of expression templates that our referring expressions use
def generate_templates(shapedict):

    templatedict = {}

    #"<col> object template"
    if "red objects" in shapedict:
        templatedict["red objects"] = "<col> object template"
    if "green objects" in shapedict:
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

    #print(templatedict)

    return templatedict
    

#generate referring expressions based on the objects in attribute indexes
def generate_expressions(attribute_indexes):
    
    shapedict = {}

    # current_keys = list(attribute_indexes.keys())
    # for key in current_keys:
    #     if len(attribute_indexes[key]) == 0:
    #         del attribute_indexes[key]
    
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
    #print(shapedict)

    return shapedict


def language_controller(scene_list):
    for scene_ob in scene_list:
        print(scene_ob.image_location)
        attribute_indexes = { #when an object has one of these attributes, add its index to the list for that attribute
            "red" : [],
            "green" : [],
            "small" : [],
            "big" : [],
            "sphere" : [],
            "box" : []
        }
        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions
        filtered_expressions = list()
        for expression in full_expression_list:
            if len(expression) >= 3 and len(expression[2]) > 0:
                filtered_expressions.append(expression)

        scene_ob.list_expressions = filtered_expressions #set the attribute in the scene object
    print("finished lang expression")


def main_test_script_1():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (0,0,0))
    object_1.normalized_location = (0,0)
    object_2 = Model("small", "green", "sphere", (2,0,0))
    object_2.normalized_location = (2,0)
    #object_3 = objects("big", "red", "box", (0,1,0))
    #object_3.normalized_location = (0,1)
    #object_4 = objects("small", "green", "sphere", (2,1,0))
    #object_4.normalized_location = (2,1)
    list_object = []
    list_object.append(object_1)
    list_object.append(object_2)
    #list_object.append(object_3)
    #list_object.append(object_4)


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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)


def main_test_script_2():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (2,0,0))
    object_1.normalized_location = (2,0)
    object_2 = Model("small", "green", "sphere", (0,0,0))
    object_2.normalized_location = (0,0)
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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

def main_test_script_3():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (0,2,0))
    object_1.normalized_location = (0,2)
    object_2 = Model("small", "green", "sphere", (0,0,0))
    object_2.normalized_location = (0,0)
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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

def main_test_script_4():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (1,2,0))
    object_1.normalized_location = (1,2)
    object_2 = Model("small", "green", "sphere", (0,0,0))
    object_2.normalized_location = (0,0)
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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

def main_test_script_5():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (2,0,0))
    object_1.normalized_location = (2,0)
    object_2 = Model("small", "green", "sphere", (1,2,0))
    object_2.normalized_location = (1,2)
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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

def main_test_script_6():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("big", "red", "box", (2,1,0))
    object_1.normalized_location = (2,1)
    object_2 = Model("small", "green", "sphere", (1,1,0))
    object_2.normalized_location = (1,1)
    object_3 = Model("small", "red", "sphere", (0, 1, 0))
    object_3.normalized_location = (0,1)
    list_object = []
    list_object.append(object_1)
    list_object.append(object_2)
    list_object.append(object_3)

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

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

def main_test_script_8():

    #for testing
    list_scenes = list() #comment this line out if not testing
    

    object_1 = Model("small", "red", "box", (1,1,0))
    object_1.normalized_location = (1,1)
    object_2 = Model("small", "green", "sphere", (1,2,0))
    object_2.normalized_location = (1,2)

    list_object = []
    list_object.append(object_1)
    list_object.append(object_2)

    scene_1 = Scene("", list_object)

    object_3 = Model("big", "red", "sphere", (0,0,0))
    object_3.normalized_location = (0,0)
    object_4 = Model("small", "green", "sphere", (0,-2,0))
    object_4.normalized_location = (0,-2)
    object_5 = Model("small", "red", "box", (2,0,0))
    object_5.normalized_location = (2,0)

    list_object = []
    list_object.append(object_3)
    list_object.append(object_4)
    list_object.append(object_5)

    #scene_2 = Scene("", list_object)

    list_scenes.append(scene_1)
    #list_scenes.append(scene_2)
    


    for scene_ob in list_scenes:

        attribute_indexes = { #when an object has one of these attributes, add its index to the list for that attribute
            "red" : [],
            "green" : [],
            "small" : [],
            "big" : [],
            "sphere" : [],
            "box" : []
        }

        for index, item in enumerate(scene_ob.model_list): #make tuple/list for each object like: (1, red, box, small) 
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
        full_expression_list = expressionlist + location_expressions

        scene_ob.list_expressions = full_expression_list #set the attribute in the scene object


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
        print()
        print("FULL EXPRESSION LIST: ")
        print(full_expression_list)

if __name__ == "__main__":
    main_test_script_1()
