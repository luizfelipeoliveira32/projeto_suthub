from app.database import enrollments_collection
from app.processor.enrollment_processor import process_enrollment
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import logging
import os
import random
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["suthub_db"]
enrollments = db["enrollments"]

async def process_one_enrollment(collection=None):
    if collection is None:
        client = AsyncIOMotorClient("mongodb://mongo:27017")
        db = client["suthub_db"]
        collection = db["enrollments"]

    doc = await collection.find_one({"status": "processing"})
    if not doc:
        return False

    logger.info(f"⌛ Processando inscrição: {doc.get('name', 'N/A')} ({doc.get('cpf', 'N/A')})")

    # Simula tempo de processamento mínimo de 2 segundos
    await asyncio.sleep(2)

    new_status = random.choice(["accepted", "rejected"])

    await collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {"status": new_status}}
    )

    logger.info(f"✅ Inscrição de {doc.get('name', 'N/A')} atualizada para '{new_status}'")

    return True


async def process_queue():
    while True:
        processed = await process_one_enrollment()
        if not processed:
            logger.info("📭 Nenhuma inscrição pendente. Aguardando...")
            await asyncio.sleep(2)