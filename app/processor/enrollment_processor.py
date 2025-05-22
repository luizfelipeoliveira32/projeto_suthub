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

'''async def process_enrollments():
    while True:
        # Busca a primeira matrícula pendente
        enrollment = await enrollments.find_one({"status": "pending"})
        if enrollment:
            logger.info(f"Processing: {enrollment['cpf']} - {enrollment['name']}")
            await asyncio.sleep(2)  # simula tempo de processamento

            # Regra arbitrária: CPF termina em par = aprovado
            last_digit = int(enrollment["cpf"][-1])
            new_status = "approved" if last_digit % 2 == 0 else "rejected"

            await enrollments.update_one(
                {"_id": enrollment["_id"]},
                {"$set": {"status": new_status}}
            )
            logger.info(f"{enrollment['cpf']} status: {new_status}")
        else:
            await asyncio.sleep(1)  # espera antes de tentar novamente

if __name__ == "__main__":
    asyncio.run(process_enrollments())
'''