import pytest

from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db

from tests.fixtures import app, client, agency


def test_register_customer(client,agency):


    response = client.post("/customer/", json={
        "name": "Aaron Rodgers",
        "address": "Rockefeller Street 43, 3792 New York",
        "email": "AR8@nfljets.us",
        "budget": 25000,
        "preference": "Germany"
    })

    assert response.status_code == 200

    parsed = response.get_json()
    customer_response = parsed["customer"]

    assert customer_response["name"] == "Aaron Rodgers"
    assert customer_response["address"] == "Rockefeller Street 43, 3792 New York"
    assert customer_response["email"] == "AR8@nfljets.us"
    assert customer_response["budget"] == 25000
    assert customer_response["preference"] == "Germany"


def test_register_customer_errors(client,agency):

    response1 = client.post("/customer/", json={
        "name":"Mark Zuckerberg",
        "address": "8th Avenue 5, 3728 Manhattan",
        "email":"Mark@meta.com",
        "budget": 0,
        "preference": "String"
    })

    assert response1.status_code == 400

    parsed1 = response1.get_json()
    error1 = parsed1["message"]

    assert error1 == "Please enter a valid budget"

    response2 = client.post("/customer/", json={
        "name": "Stephen Hawking",
        "address": "Richard's Street 32, 4728 Oxford",
        "email": "Stephen@hawking.co.uk",
        "budget": 20000,
        "preference": "String"
    })

    assert response2.status_code == 400

    parsed2 = response2.get_json()
    error2 = parsed2["message"]

    assert error2 == "Customer already registered"