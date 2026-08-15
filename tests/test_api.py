from dotenv import load_dotenv

load_dotenv(".env.test")
from fastapi.testclient import TestClient
from main import app





client = TestClient(app)


def test_get_tasks_without_authentication():
    response = client.get("/tasks")

    assert response.status_code == 401