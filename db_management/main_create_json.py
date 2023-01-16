import os
import create_json


def read_files():
    dir_path = input("Insert the path of the directory that contains ONLY the txt files: ")
    for file_to_read in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_to_read)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                if f.name.endswith(".txt"):
                    output_path = "files/json_files"
                    output = file_to_read.replace(".txt", ".json")
                    print("Creating json of: ", output)
                    output = open(os.path.join(output_path, output), "w")
                    create_json.create_file_json(f, output)
    print("The creation of the json files to insert into mongodb has finished.\n")
    return "files/json_files"
