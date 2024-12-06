from pymongo import MongoClient

# Initialize the MongoDB client
mongo_client = MongoClient("mongodb://localhost:27017")

# Access the database and collection
database = mongo_client["stroke_db"]
patients_collection = database["patient_tb"]

def mongo_insert(data):
    """
    Function to insert a single document into the patient_tb collection.
    """
    patients_collection.insert_one(data)
