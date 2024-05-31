import pytest

from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db

from tests.fixtures import app, client, agency


def test_add_country(client,agency):

    response = client.post("/country/",json={
        "name": "Monaco"
    })

    assert response.status_code == 200

    parsed = response.get_json()
    country_response = parsed["country"]

    assert country_response["name"] == "Monaco"


def test_add_country_error(client,agency):


    country_response = client.post("/country/", json={
        "name": "Germany"
    })


    assert country_response.status_code == 400

    parsed = country_response.get_json()
    error = parsed["message"]

    assert error == "This country is already registered"