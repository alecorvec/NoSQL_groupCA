import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_PORT = int(os.getenv("MONGODB_PORT"))
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(MONGODB_URL, MONGODB_PORT)
db = client[DB_NAME]

air = db.get_collection("air")
energy = db.get_collection("energy")

# rev = db.get_collection("Reviews")
# if (db.get_collection("Reviews") == None):
#     rev = db.create_collection("Reviews")
# print("Drop db ? yes/no")
# perm = input()
# if (perm == "yes" or perm == "y"):
#     rev.drop()
# rev.insert_many(documents)

while (1):
    # os.system('cls' if os.name == 'nt' else 'clear')
    # print("Add new document ? yes/no")
    # res = input()
    # if (res == "yes" or res == "y"):
    #     print("name:")
    #     name = input()
    #     print("rating:")
    #     rating = int(input())
    #     print("cuisine:")
    #     cuisine = input()
    #     document = {"name": name, "rating": rating, "cuisine": cuisine}
    #     rev.insert_one(document)
    # elif (res == "no" or res == "n"):
    #     break

if __name__ == "__main__":
    # print(rev)