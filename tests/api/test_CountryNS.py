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


def test_get_all_countries(client, agency):

    count = Country.query.count()

    response = client.get("/country/")

    assert response.status_code == 200

    parsed = response.get_json()
    countries_response = parsed["countries"]

    assert count == len(countries_response)


def test_get_country_by_id(client, agency):

    country = db.session.query(Country).filter_by(country_id=919).first()

    country_id = country.country_id

    response = client.get(f"/country/{country_id}")

    assert response.status_code == 200

    parsed = response.get_json()

    assert parsed["country_id"] == 919
    assert parsed["name"] == "Netherlands"
    assert len(parsed["activities"]) == 0

def test_get_country_by_id_error(client,agency):

    response = client.get("/country/482")

    assert response.status_code == 400

    parsed = response.get_json()

    error = parsed["message"]

    assert error == "country not found"