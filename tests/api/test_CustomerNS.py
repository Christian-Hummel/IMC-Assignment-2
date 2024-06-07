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

