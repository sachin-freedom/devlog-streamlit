# db.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)

# Access collections easily
db = client["devlog"]
users = db["users"]
logs = db["logs"]
