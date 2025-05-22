from enrollment_processor import process_enrollment
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["suthub_db"]
enrollments = db["enrollments"]

def process_queue():
    while True:
        doc = db["enrollment_queue"].find_one_and_update(
            {"status": "PENDING"},
            {"$set": {"status": "PROCESSING"}},
            sort=[("created_at", 1)]
        )

        if doc:
            logger.info("⌛ Processando:", doc["data"])
            time.sleep(2)  # ✅ Delay obrigatório
            process_enrollment(doc["data"])
            db["enrollment_queue"].update_one(
                {"_id": doc["_id"]},
                {"$set": {"status": "DONE"}}
            )
        else:
            time.sleep(1)

if __name__ == "__main__":
    process_queue()
