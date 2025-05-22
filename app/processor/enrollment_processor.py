import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["suthub_db"]
enrollments = db["enrollments"]


def process_enrollment(data):
    db["enrollments"].insert_one(data)
    logger.info(f"✅ Inscrição salva: {data}")