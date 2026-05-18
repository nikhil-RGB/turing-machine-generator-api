from .utils import *
from routers.auth import get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db


def test_create_user_success(test_user):
    response = client.post("/auth/create_user", json={"username": "newuser", "password": "password123"})
    assert response.status_code == status.HTTP_201_CREATED



def test_create_user_duplicate_username(test_user):
    response = client.post("/auth/create_user", json={"username": "testuser", "password": "different"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(test_user):
    response = client.post("/auth/token", data={"username": "testuser", "password": "testpass123"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(test_user):
    response = client.post("/auth/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user():
    response = client.post("/auth/token", data={"username": "nobody", "password": "password123"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
