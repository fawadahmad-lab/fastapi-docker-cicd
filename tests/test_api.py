from dotenv import load_dotenv
load_dotenv(".env.test")

import json
import uuid

from fastapi.testclient import TestClient
from main import app
from redis_client import redis_client

client = TestClient(app)


def test_get_tasks_without_authentication():
    response = client.get("/tasks")

    assert response.status_code == 401


def test_get_tasks_populates_redis_cache():
    unique_id = uuid.uuid4().hex[:8]

    username = f"redis_test_user_{unique_id}"
    email = f"redis_test_{unique_id}@example.com"
    password = "testpassword123"

    # Create test user
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )

    assert signup_response.status_code == 201

    user = signup_response.json()
    user_id = user["id"]

    cache_key = f"tasks:user:{user_id}"

    # Make sure we're starting clean
    redis_client.delete(cache_key)

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Get tasks
    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
    )

    assert response.status_code == 200

    # Verify Redis cache was populated
    cached_data = redis_client.get(cache_key)

    assert cached_data is not None

    cached_tasks = json.loads(cached_data)

    assert isinstance(cached_tasks, list)