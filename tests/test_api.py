from dotenv import load_dotenv

load_dotenv(".env.test")

from fastapi.testclient import TestClient

from main import app
from database import Base, engine


Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)