import json



def read_tree_from_json(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    # print(json_object)
    # print(type(json_object))
    return json_object
