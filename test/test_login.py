from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from config.db import create_db_engine
from main import app
from models.data.orrs import Login
from utils.auth_session import get_current_user

client = TestClient(app)


def db_connect():
    client_od = AsyncIOMotorClient(f"mongodb://localhost:27017/")
    engine = AIOEngine(client=client_od, database="orrs_test")
    return engine


async def get_user():
    return Login(
        **{
            "username": "testuser",
            "login_id": 100,
            "password": "testpassword",
            "passphrase": None,
            "profile": None,
        }
    )


app.dependency_overrides[get_current_user] = get_user
app.dependency_overrides[create_db_engine] = db_connect


def test_list_login():
    response = client.get("/api/v1/login/list/all")
    assert response.status_code == 201
