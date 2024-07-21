import os
import pymongo

mongo_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
client = pymongo.MongoClient(mongo_url)
db = client["word_database"]

words_collection = db["words"]
