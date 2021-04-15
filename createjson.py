import json
import os

def createjsonfile(folder_name, sceneList, json_file_path):
    output_list = list()
    for idx, sc in enumerate(sceneList):

        for idy, expression in enumerate(sc.list_expressions):
            ref_expr, template, _ = expression
            local_dict = dict()
            local_dict["expression"] = ref_expr
            local_dict["template"] = template
            local_dict["output_image"] = "{}/{}_{}.jpg".format(folder_name, idx, idy)
            local_dict["original_image"] = sc.image_location
            output_list.append(local_dict)

    json_string = json.dumps(output_list)
    with open(json_file_path) as f:
        f.write(json_string)
        f.close()

if __name__ == "__main__":
    folder = "generated.json"
    #sceneList?
    path = os.getcwd()

    createjson(folder, sceneList, path)

