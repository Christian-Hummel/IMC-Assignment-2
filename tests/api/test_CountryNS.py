import pytest

from src.database import Supervisor, TravelAgent, Customer, Country, Activity, User, db

from tests.fixtures import app, client, agency

# Country
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


def test_get_all_countries_error(client,agency):

    empty = db.session.query(Country).delete()
    db.session.commit()

    response_countries = client.get("/country/")

    assert response_countries.status_code == 400

    parsed_countries = response_countries.get_json()
    countries_error = parsed_countries["message"]

    assert countries_error == "There are no countries registered in the agency"

def test_get_country_by_id_error(client,agency):

    response = client.get("/country/482")

    assert response.status_code == 400

    parsed = response.get_json()

    error = parsed["message"]

    assert error == "country not found"

# Activity

def test_add_activity(client,agency):


    country = db.session.query(Country).filter_by(country_id=915).first()

    country_id = country.country_id

    response = client.post(f"/country/{country_id}/activity", json={
        "name":"zoo",
        "price":40
    })

    assert response.status_code == 200

    parsed = response.get_json()
    activity_response = parsed["activity"]

    assert activity_response["name"] == "zoo"
    assert activity_response["price"] == 40


def test_add_activity_error(client,agency):

    response = client.post("/country/914/activity", json={
        "name":"city tour",
        "price": 0,
    })

    assert response.status_code == 400

    parsed = response.get_json()
    error = parsed["message"]

    assert error == "Please enter a valid price for this activity"


def test_update_activity(client,agency):

    country = db.session.query(Country).filter_by(name="Brazil").first()
    country_id = country.country_id

    activity_response = client.post(f"/country/{country_id}/activity", json={
        "name": "Bus Tour",
        "price": 45
    })

    parsed_activity = activity_response.get_json()
    response_activity = parsed_activity["activity"]

    activity_id = response_activity["activity_id"]

    update_response = client.post(f"/country/{country_id}/activity/update", json={
        "activity_id": activity_id,
        "name": "City Tour",
        "price": 50
    })

    assert update_response.status_code == 200

    parsed_update = update_response.get_json()
    response_update = parsed_update["activity"]

    # this activity already exists for another country, so check for updated id
    assert response_update["activity_id"] == 614

    assert response_update["name"] == "City Tour"
    assert response_update["price"] == 50


def test_update_activity_errors(client,agency):

    response_country = client.post(f"/country/423/activity/update", json={
        "activity_id": 603,
        "name": "London Leg",
        "price": 50
    })

    assert response_country.status_code == 400

    parsed_country = response_country.get_json()
    country_error = parsed_country["message"]

    assert country_error == "Country not found"

    response_activity = client.post(f"country/903/activity/update",json={
        "activity_id": 502,
        "name": "London Alley",
        "price": 70
    })

    assert response_activity.status_code == 400

    parsed_activity = response_activity.get_json()
    activity_error = parsed_activity["message"]

    assert activity_error == "Activity not found"

    response_default1 = client.post(f"country/903/activity/update",json={
        "activity_id": 603,
        "name": "London Eye",
        "price": 50
    })

    assert response_default1.status_code == 400

    parsed_default1 = response_default1.get_json()
    default_error1 = parsed_default1["message"]

    assert default_error1 == "Please insert values to be updated"

    response_default2 = client.post(f"country/903/activity/update",json={
        "activity_id": 603,
        "name": "string",
        "price": 50
    })

    assert response_default1.status_code == 400

    parsed_default2 = response_default2.get_json()
    default_error2 = parsed_default2["message"]

    assert default_error2 == "Please insert values to be updated"

