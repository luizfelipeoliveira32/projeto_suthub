from pymongo import MongoClient
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["suthub_db"]
enrollments = db["enrollments"]

def enqueue_enrollment(data):
    db["enrollment_queue"].insert_one({
        "data": data,
        "status": "PENDING",
        "created_at": datetime.now()
    })
