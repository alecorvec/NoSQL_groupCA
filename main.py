import os
from dotenv import load_dotenv
import pymongo
import json

MENU_CODE = 0
BACK_CODE = 1
EXIT_CODE = 2

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_PORT = int(os.getenv("MONGODB_PORT"))
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(MONGODB_URL, MONGODB_PORT)
db = client[DB_NAME]

en_col = db.get_collection("energy")
ai_col = db.get_collection("air")
re_col = db.get_collection("recycling")
if (db.get_collection("energy") == None):
    en_col = db.create_collection("energy")
if (db.get_collection("air") == None):
    ai_col = db.create_collection("air")
if (db.get_collection("recycling") == None):
    re_col = db.create_collection("recycling") 
print("Drop db ? yes/no")
perm = input()
if (perm == "yes" or perm == "y"):
    en_col.drop()
    ai_col.drop()
    re_col.drop()
    

nb_col = 3

col_arr = {
    "energy": en_col,
    "air": ai_col,
    "recycling": re_col
}
    
def basic_print():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Interactive DB interface (Type MENU at any point to go back to the menu, BACK to go back to previous page), EXIT to quit")
    print("________________________________________")
    
    
def read_col(col):
    basic_print()
    print(f"Reading documents from the collection '{col.name}'")
    documents = list(col.find())
    if not documents:
        print("No documents found in this collection.")
    else:
        for doc in documents:
            print(json.dumps(doc, indent=4, default=str))
    input("Press Enter to go back")
    return BACK_CODE


def create_col(col):
    basic_print()
    print(f"Creating a new document in the collection '{col.name}'")
    print("Enter the document as a valid JSON string:")
    try:
        doc_str = input()
        document = json.loads(doc_str)
        col.insert_one(document)
        print("Document inserted successfully!")
    except json.JSONDecodeError:
        print("Invalid JSON format. Document not created.")
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to go back")
    return BACK_CODE


def update_col(col):
    basic_print()
    print(f"Updating a document in the collection '{col.name}'")
    print("Enter the filter query to find the document (as a JSON string):")
    try:
        filter_str = input()
        filter_query = json.loads(filter_str)
        print("Enter the update query (as a JSON string):")
        update_str = input()
        update_query = {"$set": json.loads(update_str)}
        result = col.update_one(filter_query, update_query)
        if result.matched_count > 0:
            print("Document updated successfully!")
        else:
            print("No matching document found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to go back")
    return MENU_CODE


def delete_col(col):
    basic_print()
    print(f"Deleting documents from the collection '{col.name}'")
    print("Enter the filter query to find documents to delete (as a JSON string):")
    try:
        filter_str = input()
        filter_query = json.loads(filter_str)
        result = col.delete_many(filter_query)
        print(f"{result.deleted_count} document(s) deleted.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")
    input("Press Enter to go back")
    return MENU_CODE

def options(col_in, col_name, col):
    code = 3
    if (col_in == "READ"):
        code = read_col(col)
    elif (col_in == "CREATE"):
        code = create_col(col)
    elif (col_in == "UPDATE"):
        code = update_col(col)
    elif (col_in == "DELETE"):
        code = delete_col(col)
    return code

def col_loop(col_name, col):
    while (1):
        basic_print()
        print("'" + col_name + "'" + " collection :")
        print("________________________________________")
        print("READ collection")
        print("CREATE document")
        print("UPDATE document")
        print("DELETE document")
        print("________________________________________")
        print("Type an option :")
        col_in = input()
        if (col_in == "MENU"):
            return MENU_CODE
        elif (col_in == "BACK"):
            return BACK_CODE
        elif (col_in == "EXIT"):
            return EXIT_CODE
        options(col_in, col_name, col)


def main_loop(db, col, nb_col):
    while (1):
        basic_print()
        print("Choose a collection :")
        print("________________________________________")
        print("energy")
        print("air")
        print("recycling")
        print("________________________________________")
        print("Collection :")
        col_in = input()
        if (col_in == "EXIT" or col_in == "BACK"):
            break
        elif (col_in == "energy" or col_in == "air" or col_in == "recycling"):
            code = col_loop(col_in, col[col_in])
            if (code == EXIT_CODE):
                break


if __name__ == "__main__":
    main_loop(db, col_arr, nb_col)
    os.system('cls' if os.name == 'nt' else 'clear')
