import main_create_json
import mongo_services


def menu():
    print("Welcome, what would you like to do?"),
    print("1. Insert a txt file (with one or more rna sequences) into mongodb."),
    print("2. Modify a single rna sequence."),
    print("3. Delete a single rna sequence."),
    print("4. Delete all."),
    print("0. Exit."),
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
        mongo_services.insert_many_to_mongo(output_path)
        menu()
    elif result == 2:
        print("You chose to update one document of mongo db.")
        mongo_services.update_one_field()
        menu()
    elif result == 3:
        print("You chose to delete one document of mongo db.")
        mongo_services.delete_one()
        menu()
    elif result == 4:
        print("You chose to delete all documents in a collection.")
        mongo_services.delete_all()
        menu()


menu()