import logging
import pytest
from fastapi.testclient import TestClient
from api.main import app

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

client = TestClient(app)
    
@pytest.mark.asyncio
async def test_return_templates():
    logger.info("Тестируем получение существующей страницы")
    response = client.get("/api/templates/sports")
    assert response.status_code == 200
    
def test_create_item():
    logger.info("Тестируем создание сущности Sport")
    response = client.post(
        "/api/sports/", json={"name": "Тестовый", "trainer": "Тестер Тестерович"}
    )
    assert response.status_code == 200
    assert response.json() == {}
    
@pytest.mark.asyncio
async def test_return_templates_2():
    logger.info("Тестируем получение несуществующей страницы")
    response = client.get("/api/templates/users")
    assert response.status_code == 200
    
def test_put_item():
    logger.info("Тестируем обновление сущности Sport")
    response = client.put(
        "/api/sports/1", json={"id": 1, "name": "Тестовый", "trainer": "Тестер Тестерович"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Тестовый", "trainer": "Тестер Тестерович"}
    