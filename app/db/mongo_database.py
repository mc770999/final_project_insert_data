import os

from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv(verbose=True)


client = MongoClient(os.getenv("DATABASE_MONGO_URL"))

# Access a database (creates it if it doesn't exist)
db = client["final_project"]
event_collection = db["events"]


