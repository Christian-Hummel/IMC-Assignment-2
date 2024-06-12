import pytest

from src.database import Supervisor, TravelAgent, Offer, Customer, Country, Activity, User, db

from tests.fixtures import app, client, agency


def test_update_agent(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=305).first()
    employee_id = agent.employee_id

    assert agent.address == "Juniper Drive 112, 7788 Themyscira"

    response = client.post(f"/travelAgent/{employee_id}/update", json= {
        "name": "Isabella Moore",
        "address": "Highway Drive 112, 7788 Themyscira"
    })

    assert response.status_code == 200

    parsed = response.get_json()
    update_response = parsed["travelAgent"]

    assert update_response["name"] == "Isabella Moore"
    assert update_response["address"] == "Highway Drive 112, 7788 Themyscira"

def test_update_agent_errors(client,agency):


    default_agent = db.session.query(TravelAgent).filter_by(employee_id=255).first()
    employee_id = default_agent.employee_id

    response_format1 = client.post(f"/travelAgent/{employee_id}/update", json={
        "name": "string",
        "address": "Elm Street 12, 5678 Gotham"
    })

    assert response_format1.status_code == 400

    parsed_format1 = response_format1.get_json()
    format_error1 = parsed_format1["message"]

    assert format_error1 == "Please enter first and last name seperated by a space"

    response_format2 = client.post(f"/travelAgent/{employee_id}/update", json={
        "name": "LucasKendall",
        "address": "Elm Street 12, 5678 Gotham"
    })

    assert response_format2.status_code == 400

    parsed_format2 = response_format2.get_json()
    format_error2 = parsed_format2["message"]

    assert format_error2 == "Please enter first and last name seperated by a space"

    response_default1 = client.post(f"/travelAgent/{employee_id}/update", json={
        "name": "Jane Smith",
        "address": "string"
    })

    assert response_default1.status_code == 400

    parsed_default1 = response_default1.get_json()
    default_error1 = parsed_default1["message"]

    assert default_error1 == "Please insert values to be updated"

    response_default2 = client.post(f"/travelAgent/{employee_id}/update", json={
        "name": "Jane Smith",
        "address": "Elm Street 12, 5678 Gotham"
    })

    assert response_default2.status_code == 400

    parsed_default2 = response_default2.get_json()
    default_error2 = parsed_default2["message"]

    assert default_error2 == "Please insert values to be updated"

    response_nagent = client.post(f"/travelAgent/765/update", json={
        "name": "Lucas Kendall",
        "address": "Elm Street 12, 5678 Gotham"
    })

    assert response_nagent.status_code == 400

    parsed_nagent = response_nagent.get_json()
    nagent_error2 = parsed_nagent["message"]


def test_present_new_offer(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=305).first()
    customer = db.session.query(Customer).filter_by(customer_id=714).first()
    country = db.session.query(Country).filter_by(country_id=901).first()

    employee_id = agent.employee_id
    customer_id = customer.customer_id
    country_name = country.name



    response_offer = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": country_name,
        "activities": [
            601
        ]
    })


    assert response_offer.status_code == 200

    #print(response_offer.get_json())



    offer = db.session.query(Offer).filter_by(offer_id=801).first()

    print(agent.employee_id)
    print([activity.name for activity in offer.activities])
    print(offer.total_price)
    print(offer.customer_id)

    assert offer.offer_id != 0
    assert offer.customer_id == 714
    assert offer.country == "Germany"
    assert offer.agent_id == 305
    assert offer.status == "pending"
    assert offer.total_price == 6000




