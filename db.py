# db.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_URI = st.secrets["MONGO_URI"] if "MONGO_URI" in st.secrets else os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)

# Access collections easily
db = client["devlog"]
users = db["users"]
logs = db["logs"]
