from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client["suthub_db"]

age_groups_collection = db["age_groups"]
enrollments_collection = db["enrollments"]
