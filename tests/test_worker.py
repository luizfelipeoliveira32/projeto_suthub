import pytest
import pytest_asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.processor.worker import process_one_enrollment

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

TEST_DB_NAME = "test_db"
TEST_COLLECTION_NAME = "enrollments"


# Fixture para o cliente do MongoDB
@pytest_asyncio.fixture
async def db_client():
    client = AsyncIOMotorClient("mongodb://mongo:27017")
    yield client
    client.close()


# Fixture para a collection de inscrições de teste
@pytest_asyncio.fixture
async def enrollments_collection(db_client):
    db = db_client[TEST_DB_NAME]
    collection = db[TEST_COLLECTION_NAME]
    await collection.delete_many({})
    return collection


@pytest.mark.asyncio
async def test_process_one_enrollment(enrollments_collection):
    test_doc = {
        "name": "Joao",
        "cpf": "00011122233",
        "status": "processing"
    }
    insert_result = await enrollments_collection.insert_one(test_doc)

    await process_one_enrollment(collection=enrollments_collection)

    updated_doc = await enrollments_collection.find_one({"_id": insert_result.inserted_id})
    assert updated_doc["status"] in ["accepted", "rejected"], (
        f"Falha ao processar inscrição: {updated_doc}. Esperado 'accepted' ou 'rejected'"
    )
    logger.info(f"✅ Teste bem-sucedido: CPF %s, status atualizado para '%s'", updated_doc["cpf"], updated_doc["status"])


@pytest.mark.asyncio
async def test_process_one_enrollment_no_pending(enrollments_collection):
    test_doc = {
        "name": "Maria",
        "cpf": "99988877766",
        "status": "completed"
    }
    await enrollments_collection.insert_one(test_doc)

    await process_one_enrollment(collection=enrollments_collection)

    unchanged_doc = await enrollments_collection.find_one({"cpf": "99988877766"})
    assert unchanged_doc["status"] == "completed", (
        f"Status alterado indevidamente para {unchanged_doc['status']} para CPF {unchanged_doc['cpf']}"
    )
    logger.info(f"✅ Teste bem-sucedido: CPF %s, status permaneceu '%s'", unchanged_doc["cpf"], unchanged_doc["status"])