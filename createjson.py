import json
import os

def createjsonfile(folder_name, sceneList, json_file_path):
    output_list = list()
    for idx, sc in enumerate(sceneList):

        for idy, expression in enumerate(sc.list_expressions):
            ref_expr, template, objects_indices = expression
            local_dict = dict()
            local_dict["expression"] = ref_expr
            local_dict["template"] = template
            local_dict["output_image"] = "{}/{}_{}.jpg".format(folder_name, idx, idy)
            local_dict["original_image"] = sc.image_location
            local_dict["scene_objects"] = list()
            for index, model in enumerate(sc.model_list):
                m = dict()
                m["index"] = index
                m["color"] = model.color
                m["shape"] = model.shape
                m["size"] = model.size
                local_dict["scene_objects"].append(m)
            local_dict["expression_objects"] = list()
            for i in objects_indices:
                local_dict["expression_objects"].append(i)
            output_list.append(local_dict)

    json_string = json.dumps(output_list, indent=4)
    with open(json_file_path, "w") as f:
        f.write(json_string)
        f.close()

if __name__ == "__main__":
    folder = "generated.json"
    #sceneList?
    path = os.getcwd()

    

