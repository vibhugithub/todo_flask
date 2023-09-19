import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
Database = client["todoapp"]


def insert(collection_name,query):
    # specified collection
    collection = Database[collection_name]

    return collection.insert_one(query)

def find_one(collection_name,query):
    # specified collection
    collection = Database[collection_name]

    return collection.find_one(query)

def find(collection_name,query):
    # specified collection
    collection = Database[collection_name]

    return collection.find(query)

def delete_one(collection_name,query):
    # specified collection
    collection = Database[collection_name]

    return collection.delete_one(query)

def update_one(collection_name,query,filter_expression):
    # specified collection
    collection = Database[collection_name]

    return collection.update_one(query,filter_expression)