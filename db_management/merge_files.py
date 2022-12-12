def merge_files():
    path_1 = input("Insert the path of the first file: ")
    path_2 = input("Insert the path of the second file: ")
    output_path = input("Insert the path of the result file: ")
    file_1 = open(path_1, 'r')
    file_2 = open(path_2, 'r')
    output_file = open(output_path, 'w')
    for line in file_1:
        output_file.write(line)
    for line in file_2:
        output_file.write(line)


merge_files()
