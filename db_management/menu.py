import main_create_json
import mongo_services


# It's a menu that allows the user to choose what to do.
# :return: The menu() function is being returned.
def menu():
    print("Welcome, what would you like to do?")
    print("1. Insert rna_sequences files (.txt) into mongodb.")
    print("2. Insert additional files (.dbn, .fasta, .ct, .bpseq, with and without header).")
    print("3. Modify a single rna sequence.")
    print("4. Delete a single rna sequence.")
    print("5. Delete all.")
    print("0. Exit.")
    result = input("Insert the number of the action you want to do: ")
    if not result.isnumeric():
        print("Sorry, you have to insert a number.")
        menu()
    else:
        result = int(result)
    if result == 0:
        return
    elif result == 1:
        print("You chose to insert one or more txt files into mongo db.")
        output_path = main_create_json.read_files()
        mongo_services.insert_to_mongo(output_path)
        menu()
    elif result == 2:
        mongo_services.insert_files()
        menu()
    elif result == 3:
        print("You chose to update one document of mongo db.")
        mongo_services.update_one_field()
        menu()
    elif result == 4:
        print("You chose to delete one document of mongo db.")
        mongo_services.delete_one()
        menu()
    elif result == 5:
        print("You chose to delete all documents in a collection.")
        mongo_services.delete_all()
        menu()


menu()
