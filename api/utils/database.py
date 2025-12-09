from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.mongo_uri = os.environ.get('MONGODB_URI')
        self.client = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client['tiktok_db']
            print("Connected to MongoDB")
            return self.db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None
    
    def get_collection(self, collection_name):
        if self.db is None:
            self.connect()
        return self.db[collection_name]

# Singleton instance
db = Database()
