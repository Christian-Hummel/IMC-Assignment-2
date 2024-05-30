import pytest

from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db

from tests.fixtures import app, client, agency


def test_add_supervisor(client,agency):

    response = client.post("/supervisor/", json={
        "name":"Warren Buffet",
        "address":"103 Avenue, 4932 New York",
        "salary": 20000,
        "nationality":"USA"
    })


    assert response.status_code == 200


    parsed = response.get_json()
    supervisor_response = parsed["supervisor"]


    assert supervisor_response["name"] == "Warren Buffet"
    assert supervisor_response["address"] == "103 Avenue, 4932 New York"
    assert supervisor_response["salary"] == 20000
    assert supervisor_response["nationality"] == "USA"


def test_add_supervisor_error(client, agency):

    response = client.post("/supervisor/", json={
        "name":"JasonBourne",
        "address":"Unknown Street 55, 2234 Dallas",
        "salary": 10000,
        "nationality": "USA"
    })


    assert response.status_code == 400

    parsed = response.get_json()
    error = parsed["message"]

    assert error == "Please insert your first and last name seperated by a space"


def test_register_supervisor(client,agency):

    supervisor = db.session.query(Supervisor).filter_by(employee_id=135).first()

    supervisor_id = supervisor.employee_id

    response = client.post(f"/supervisor/{supervisor_id}/register",json={
        "username":"Mark",
        "password":"Hulk"
    })

    assert response.status_code == 200

    parsed = response.get_json()
    user_response = parsed["user"]

    assert user_response["id"] == 1
    assert user_response["username"] == "Mark"


def test_register_supervisor_errors(client,agency):


    supervisor = db.session.query(Supervisor).filter_by(employee_id=13).first()

    supervisor_id = supervisor.employee_id

    response = client.post(f"/supervisor/{supervisor_id}/register", json={
        "username": "Harry",
        "password": "Stylish"
    })


    response1 = client.post(f"/supervisor/{supervisor_id}/register", json={
        "username": "Harry",
        "password": "Music"
    })

    assert response1.status_code == 400

    parsed=response1.get_json()
    error_response1 = parsed["message"]

    assert error_response1 == "This user already exists"

    response2 = client.post(f"/supervisor/734/register", json={
        "username": "Markus",
        "password": "Styles"
    })

    assert response2.status_code == 400

    parsed_nfound = response2.get_json()
    error_response2 = parsed_nfound["message"]

    assert error_response2 == "Supervisor not found"

