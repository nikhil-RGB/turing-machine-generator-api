from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext
from database import Base
from main import app
from models import Machines, Users
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'testuser', 'id': 1}


client = TestClient(app)


@pytest.fixture
def test_user():
    user = Users(
        id=1,
        username='testuser',
        hashed_password=bcrypt_context.hash('testpass123'),
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_machine():
    machine = Machines(
        id=1,
        name='TestMachine',
        group_name='TestGroup',
        machine_data=(
            '{"initial_config":"B",'
            '"configs":[{"m_config":"B","symbol":""},{"m_config":"Q","symbol":""},{"m_config":"Q","symbol":"0"}],'
            '"behaviours":[{"actions":[{"symbol":"0","type":"P"},{"symbol":"","type":"R"}],"f_config":"Q"},'
            '{"actions":[{"symbol":"","type":"L"}],"f_config":"Q"},'
            '{"actions":[{"symbol":"","type":"R"},{"symbol":"0","type":"P"}],"f_config":"Q"}],'
            '"description":"Enter a description for this turing machine here"}'
        ),
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(machine)
    db.commit()
    yield machine
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM machines;"))
        connection.commit()
