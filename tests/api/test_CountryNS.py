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

def test_remove_activity(client,agency):

    country = db.session.query(Country).filter_by(country_id=904).first()
    activity = db.session.query(Activity).filter_by(activity_id=604).first()

    country_id = country.country_id
    activity_id = activity.activity_id

    response_delete = client.delete(f"/country/{country_id}/activity/delete",json={
        "activity_id": activity_id
    })


    assert response_delete.status_code == 200

    parsed = response_delete.get_json()

    assert parsed == "Activity Edingburgh Castle has been removed from Scotland"

def test_remove_activity_errors(client,agency):


    country = db.session.query(Country).filter_by(country_id=916).first()
    activity = db.session.query(Activity).filter_by(activity_id=603).first()

    country_id = country.country_id
    activity_id = activity.activity_id

    response_inv_country = client.delete("/country/438/activity/delete", json={
        "activity_id": activity_id
    })

    assert response_inv_country.status_code == 400

    parsed_country = response_inv_country.get_json()
    country_error = parsed_country["message"]

    assert country_error == "Country not found"

    response_inv_activity = client.delete(f"/country/{country_id}/activity/delete", json={
        "activity_id": 593
    })

    assert response_inv_activity.status_code == 400

    parsed_activity = response_inv_activity.get_json()
    activity_error = parsed_activity["message"]

    assert activity_error == "Activity not found"

    response_wcountry = client.delete(f"/country/{country_id}/activity/delete", json={
        "activity_id": 614
    })

    assert response_wcountry.status_code == 400

    parsed_wcountry = response_wcountry.get_json()
    wcountry_error = parsed_wcountry["message"]

    assert wcountry_error == "This activity does not belong to the specified country"


def test_get_activity_by_id(client,agency):

    country = db.session.query(Country).filter_by(country_id=901).first()
    activity = db.session.query(Activity).filter_by(activity_id=601).first()

    country_id = country.country_id
    activity_id = activity.activity_id

    response = client.get(f"/country/{country_id}/activity", json={
        "activity_id": activity_id
    })

    assert response.status_code == 200

    parsed = response.get_json()
    activity_response = parsed["activity"]

    assert activity_response["activity_id"] == 601
    assert activity_response["name"] == "Miniatur Wunderland"
    assert activity_response["price"] == 20


def test_get_activity_by_id_errors(client,agency):

    country = db.session.query(Country).filter_by(country_id=911).first()
    activity = db.session.query(Activity).filter_by(activity_id=612).first()

    country_id = country.country_id
    activity_id = activity.activity_id

    response_diffcountry = client.get(f"/country/{country_id}/activity", json={
        "activity_id": activity_id
    })

    assert response_diffcountry.status_code == 400

    parsed_diffcountry = response_diffcountry.get_json()
    diffcountry_error = parsed_diffcountry["message"]

    assert diffcountry_error == "This activity is not registered for Brazil"

    response_ncountry = client.get("/country/349/activity", json={
        "activity_id": activity_id
    })

    assert response_ncountry.status_code == 400

    parsed_ncountry = response_ncountry.get_json()
    ncountry_error = parsed_ncountry["message"]

    assert ncountry_error == "Country not found"


def test_get_country_stats(client,agency):

    country1 = db.session.query(Country).filter_by(country_id=901).first()

    country_id1 = country1.country_id

    response_stats1 = client.get(f"/country/{country_id1}/stats")

    assert response_stats1.status_code == 200

    stats_response1 = response_stats1.get_json()

    assert stats_response1["country"] == "Germany"
    assert stats_response1["total_revenue"] == 1600
    assert "Miniatur Wunderland" in stats_response1["favourite_activity"]
    assert stats_response1["visits"] == 2


    # favourite activity tied, so there are multiple Maxima

    country2 = db.session.query(Country).filter_by(country_id=907).first()

    country_id2 = country2.country_id

    response_stats2 = client.get(f"/country/{country_id2}/stats")

    assert response_stats2.status_code == 200

    stats_response2 = response_stats2.get_json()

    assert stats_response2["country"] == "Japan"
    assert stats_response2["total_revenue"] == 7000
    assert "Baseball Game" in stats_response2["favourite_activities"]
    assert "Horseriding" in stats_response2["favourite_activities"]
    assert stats_response2["visits"] == 2



def test_get_country_stats_errors(client,agency):

    country = db.session.query(Country).filter_by(country_id=908).first()

    country_id = country.country_id

    response_nvisits = client.get(f"/country/{country_id}/stats")

    assert response_nvisits.status_code == 400

    parsed_nvisits = response_nvisits.get_json()
    nvisits_error = parsed_nvisits["message"]

    assert nvisits_error == "This country has not been visited by a customer yet"

    response_ncountry = client.get("country/684/stats")

    assert response_ncountry.status_code == 400

    parsed_ncountry = response_ncountry.get_json()
    ncountry_error = parsed_ncountry["message"]

    assert ncountry_error == "Country not found"


