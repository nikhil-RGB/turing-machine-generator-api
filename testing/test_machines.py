from .utils import *
from routers.machines import get_db, get_current_user
from fastapi import status
from models import Machines

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

MACHINE_DATA = (
    '{"initial_config":"B",'
    '"configs":[{"m_config":"B","symbol":""},{"m_config":"Q","symbol":""},{"m_config":"Q","symbol":"0"}],'
    '"behaviours":[{"actions":[{"symbol":"0","type":"P"},{"symbol":"","type":"R"}],"f_config":"Q"},'
    '{"actions":[{"symbol":"","type":"L"}],"f_config":"Q"},'
    '{"actions":[{"symbol":"","type":"R"},{"symbol":"0","type":"P"}],"f_config":"Q"}],'
    '"description":"Enter a description for this turing machine here"}'
)


# --- GET /machines/ ---

def test_get_all_machines(test_machine):
    response = client.get("/machines/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'name': 'TestMachine',
        'group_name': 'TestGroup',
        'machine_data': MACHINE_DATA,
        'owner_id': 1,
    }]


def test_get_all_machines_empty():
    response = client.get("/machines/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


# --- GET /machines/{machine_id} ---

def test_get_machine_by_id(test_machine):
    response = client.get("/machines/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'name': 'TestMachine',
        'group_name': 'TestGroup',
        'machine_data': MACHINE_DATA,
        'owner_id': 1,
    }


def test_get_machine_by_id_not_found(test_machine):
    response = client.get("/machines/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Machine not found'}


# --- POST /machines/create_machine ---

def test_create_machine(test_machine):
    request = {
        'name': 'NewMachine',
        'group_name': 'NewGroup',
        'machine_data': MACHINE_DATA,
    }
    response = client.post("/machines/create_machine", json=request)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    machine_model = db.query(Machines).filter(Machines.id == 2).first()
    assert machine_model.name == request.get('name')
    assert machine_model.group_name == request.get('group_name')
    assert machine_model.machine_data == request.get('machine_data')
    assert machine_model.owner_id == 1


def test_create_machine_empty_name_rejected(test_machine):
    response = client.post("/machines/create_machine", json={
        'name': '',
        'group_name': 'TestGroup',
        'machine_data': MACHINE_DATA,
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_machine_name_too_long_rejected(test_machine):
    response = client.post("/machines/create_machine", json={
        'name': 'A' * 21,
        'group_name': 'TestGroup',
        'machine_data': MACHINE_DATA,
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# --- PUT /machines/update_machine/{id} ---

def test_update_machine(test_machine):
    request = {
        'name': 'UpdatedMachine',
        'group_name': 'UpdatedGroup',
        'machine_data': MACHINE_DATA,
    }
    response = client.put("/machines/update_machine/1", json=request)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    machine_model = db.query(Machines).filter(Machines.id == 1).first()
    assert machine_model.name == request.get('name')
    assert machine_model.group_name == request.get('group_name')


def test_update_machine_not_found(test_machine):
    response = client.put("/machines/update_machine/999", json={
        'name': 'UpdatedMachine',
        'group_name': 'UpdatedGroup',
        'machine_data': MACHINE_DATA,
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Machine not found'}


# --- DELETE /machines/delete_machine/{machine_id} ---

def test_delete_machine(test_machine):
    response = client.delete("/machines/delete_machine/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    machine_model = db.query(Machines).filter(Machines.id == 1).first()
    assert machine_model is None


def test_delete_machine_not_found(test_machine):
    response = client.delete("/machines/delete_machine/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Machine not found'}
