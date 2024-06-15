import pytest

from src.database import  TravelAgent, Offer, Customer, Country, db

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
    nagent_error = parsed_nagent["message"]

    assert nagent_error == "TravelAgent not found"


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
            601, 611
        ]
    })

    assert response_offer.status_code == 200


    parsed_offer = response_offer.get_json()
    offer_response = parsed_offer["offer"]


    assert offer_response["offer_id"] != 0
    assert offer_response["customer_id"] == 714
    assert offer_response["agent_id"] == 305
    assert offer_response["country"] == "Germany"
    assert len(offer_response["activities"]) == 2
    assert offer_response["total_price"] == 90
    assert offer_response["status"] == "pending"

def test_present_changed_offer(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=260).first()
    customer = db.session.query(Customer).filter_by(customer_id=705).first()
    country = db.session.query(Country).filter_by(country_id=905).first()

    offer = db.session.query(Offer).filter_by(offer_id=805).first()
    offer_id = offer.offer_id

    employee_id = agent.employee_id
    customer_id = customer.customer_id
    country_name = country.name

    price_before = offer.total_price
    activities_before = len(offer.activities)

    response_resend = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": offer_id,
        "customer_id": customer_id,
        "country": country_name,
        "activities": [
            605, 615
        ]
    })

    assert response_resend.status_code == 200

    parsed_resend = response_resend.get_json()
    resend_response = parsed_resend["offer"]

    assert resend_response["status"] == "changed"
    assert resend_response["offer_id"] == 805  # check if the id did not get changed/ lost in the process
    assert resend_response["total_price"] == 30 + price_before # 30 is the cost the added activity
    assert resend_response["country"] == "Poland"
    assert len(resend_response["activities"]) == activities_before + 1
    assert resend_response["customer_id"] == 705
    assert resend_response["agent_id"] == 260


def test_present_offer_errors(client,agency):
    # do not need an error for expert status, because if a customer requires one, this is
    # already checked by the assignment of the travelAgent

    agent = db.session.query(TravelAgent).filter_by(employee_id=300).first()
    customer = db.session.query(Customer).filter_by(customer_id=713).first()
    country = db.session.query(Country).filter_by(country_id=908).first()

    rcountry = db.session.query(Country).filter_by(country_id=902).first()


    offer = db.session.query(Offer).filter_by(offer_id=802).first()

    employee_id = agent.employee_id
    customer_id = customer.customer_id
    country_name = country.name

    rcountry_name = rcountry.name

    offer_id = offer.offer_id

    # country not assigned
    response_wcountry = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": country_name,
        "activities": [
            608
        ]
    })

    assert response_wcountry.status_code == 400

    parsed_wcountry = response_wcountry.get_json()
    wcountry_error = parsed_wcountry["message"]

    assert wcountry_error == "This country does not match with the preference of your customer"

    # activity not registered for this country

    response_wactivity = client.post(f"/travelAgent/{employee_id}/offer",json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": country_name,
        "activities": [
            611
        ]
    })


    assert response_wactivity.status_code == 400

    parsed_wactivity = response_wactivity.get_json()
    wactivity_error = parsed_wactivity["message"]

    assert wactivity_error == "Activity with id 611 not registered for this country"


    # Offer exceeds budget of customer

    response_budget = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602, 616
        ]
    })

    assert response_budget.status_code == 400

    parsed_budget = response_budget.get_json()
    budget_error = parsed_budget["message"]

    assert budget_error == "This offer exceeds the budget of the customer"

    # no activities

    response_nactivities = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            0
        ]
    })

    assert response_nactivities.status_code == 400

    parsed_nactivities = response_nactivities.get_json()
    nactivities_error = parsed_nactivities["message"]

    assert nactivities_error == "Please insert activities for your offer"


    # changed offer different agent

    response_diffagent = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 805,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_diffagent.status_code == 400

    parsed_diffagent = response_diffagent.get_json()
    diffagent_error = parsed_diffagent["message"]

    assert diffagent_error == "This offer was created by another TravelAgent"

    # changed offer - not found

    response_noffer = client.post(f"/travelAgent/{employee_id}/offer",json={
        "offer_id": 493,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_noffer.status_code == 400

    parsed_noffer = response_noffer.get_json()
    noffer_error = parsed_noffer["message"]

    assert noffer_error == "Offer not found"

    # changed offer no activities

    response_cnactivities = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 802,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            0
        ]
    })

    assert response_cnactivities.status_code == 400

    parsed_cnactivities = response_cnactivities.get_json()
    cnactivities_error = parsed_cnactivities["message"]

    assert cnactivities_error == "Please insert activities for your offer"

    # changed offer activity not registered

    response_cwactivity = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 802,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602, 610
        ]
    })

    assert response_cnactivities.status_code == 400

    parsed_cwactivity = response_cwactivity.get_json()
    cwactivity_error = parsed_cwactivity["message"]

    assert cwactivity_error == "Activity with id 610 not registered for this country"

    # changed offer budget

    response_cbudget = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 802,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602, 616
        ]
    })


    assert response_cbudget.status_code == 400

    parsed_cbudget = response_cbudget.get_json()
    cbudget_error = parsed_cbudget["message"]

    assert cbudget_error == "This offer exceeds the budget of the customer"

    # changed offer already declined

    response_declined = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 812,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_declined.status_code == 400

    parsed_declined = response_declined.get_json()
    declined_error = parsed_declined["message"]

    assert declined_error == "This offer is already declined by the customer"


    ## existance checks

    # Customer not assigned

    response_wcustomer = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": 714,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_wcustomer.status_code == 400

    parsed_wcustomer = response_wcustomer.get_json()
    wcustomer_error = parsed_wcustomer["message"]

    assert wcustomer_error == "This customer is not assigned to you"

    # Country not assigned to this agent

    response_wcountry = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": "Finland",
        "activities": [
            901
        ]
    })

    assert response_wcountry.status_code == 400

    parsed_wcountry = response_wcountry.get_json()
    wcountry_error = parsed_wcountry["message"]

    assert wcountry_error == "This country is not assigned to you"

    # Country not found 1

    response_ncountry1 = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": "La La Land",
        "activities": [
            901
        ]
    })

    assert response_ncountry1.status_code == 400

    parsed_ncountry1 = response_ncountry1.get_json()
    ncountry1_error = parsed_ncountry1["message"]

    assert ncountry1_error == "Country not found"

    # Country not found 2 - string

    response_ncountry2 = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": "string",
        "activities": [
            901
        ]
    })

    assert response_ncountry2.status_code == 400

    parsed_ncountry2 = response_ncountry2.get_json()
    ncountry2_error = parsed_ncountry2["message"]

    assert ncountry2_error == "Country not found"

    # Customer not found

    response_ncustomer = client.post(f"/travelAgent/{employee_id}/offer", json={
        "offer_id": 0,
        "customer_id": 548,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_ncustomer.status_code == 400

    parsed_ncustomer = response_ncustomer.get_json()
    ncustomer_error = parsed_ncustomer["message"]

    assert ncustomer_error == "Customer not found"

    # TravelAgent not found

    response_nagent = client.post(f"/travelAgent/777/offer", json={
        "offer_id": 0,
        "customer_id": customer_id,
        "country": rcountry_name,
        "activities": [
            602
        ]
    })

    assert response_nagent.status_code == 400

    parsed_nagent = response_nagent.get_json()
    nagent_error = parsed_nagent["message"]

    assert nagent_error == "TravelAgent not found"

def test_request_raise(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=375).first()

    employee_id = agent.employee_id

    response_raise = client.post(f"/travelAgent/{employee_id}/raise")

    assert response_raise.status_code == 200

    message = response_raise.get_json()

    assert message == "A request for a raise in salary has been sent"

def test_request_raise_error(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=400).first()

    employee_id = agent.employee_id

    response_alsent = client.post(f"/travelAgent/{employee_id}/raise")

    assert response_alsent.status_code == 400

    parsed_alsent = response_alsent.get_json()
    alsent_response = parsed_alsent["message"]

    assert alsent_response == "Request for raise still pending"

    response_nagent = client.post("/travelAgent/439/raise")

    assert response_nagent.status_code == 400

    parsed_nagent = response_nagent.get_json()
    nagent_error = parsed_nagent["message"]

    assert nagent_error == "TravelAgent not found"


def test_request_discount(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=370).first()
    offer = db.session.query(Offer).filter_by(offer_id=831).first()

    employee_id = agent.employee_id
    offer_id = offer.offer_id

    response_discount = client.post(f"/travelAgent/{employee_id}/offer/{offer_id}/discount", json={
        "percentage": 10
    })

    assert response_discount.status_code == 200

    message = response_discount.get_json()

    assert message == "A request for lowering the total price of Offer 831 by 10 percent has been sent"


def test_request_discount_errors(client,agency):

    # request already sent

    agent1 = db.session.query(TravelAgent).filter_by(employee_id=315).first()
    offer1 = db.session.query(Offer).filter_by(offer_id=811).first()

    employee_id1 = agent1.employee_id
    offer_id1 = offer1.offer_id

    response_alsent = client.post(f"/travelAgent/{employee_id1}/offer/{offer_id1}/discount", json={
        "percentage": 20
    })

    assert response_alsent.status_code == 400

    parsed_alsent = response_alsent.get_json()
    alsent_error = parsed_alsent["message"]

    assert alsent_error == "The request for lowering this offer is still pending"

    # wrong status

    agent2 = db.session.query(TravelAgent).filter_by(employee_id=375).first()
    offer2 = db.session.query(Offer).filter_by(offer_id=824).first()

    employee_id2 = agent2.employee_id
    offer_id2 = offer2.offer_id

    response_nav = client.post(f"/travelAgent/{employee_id2}/offer/{offer_id2}/discount", json={
        "percentage": 30
    })

    assert response_nav.status_code == 400

    parsed_nav = response_nav.get_json()
    nav_error = parsed_nav["message"]

    assert nav_error == "This offer is not available for discounts"

    # Offer does not exist

    response_noffer1 = client.post(f"/travelAgent/{employee_id1}/offer/473/discount", json={
        "percentage": 4
    })

    assert response_noffer1.status_code == 400

    parsed_noffer1 = response_noffer1.get_json()
    noffer_error1 = parsed_noffer1["message"]

    assert noffer_error1 == "Offer not found"

    # Offer belongs to different TravelAgent

    response_diffagent = client.post(f"/travelAgent/{employee_id1}/offer/816/discount", json={
        "percentage": 4
    })

    assert response_diffagent.status_code == 400

    parsed_diffagent = response_diffagent.get_json()
    diffagent_error = parsed_diffagent["message"]

    assert diffagent_error == "This offer is not one of yours"

    # TravelAgent not found

    response_nagent = client.post(f"/travelAgent/548/offer/{offer_id1}/discount", json={
        "percentage": 10
    })

    assert response_nagent.status_code == 400

    parsed_nagent = response_nagent.get_json()
    nagent_error = parsed_nagent["message"]

    assert nagent_error == "TravelAgent not found"

    # wrong input

    response_winput = client.post(f"/travelAgent/{employee_id1}/offer/{offer_id1}/discount", json={
        "percentage": 50
    })

    assert response_winput.status_code == 400

    parsed_winput = response_winput.get_json()
    winput_error = parsed_winput["message"]

    assert winput_error == "Please insert a valid percentage in the range from 1 to 40"


def test_get_all_offers(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=400).first()

    employee_id = agent.employee_id

    response_offers = client.get(f"/travelAgent/{employee_id}/offer")

    assert response_offers.status_code == 200

    parsed_offers = response_offers.get_json()
    offers_response= parsed_offers["offers"]

    assert len(offers_response) == 6

def test_get_all_offers_errors(client,agency):

    agent = db.session.query(TravelAgent).filter_by(employee_id=240).first()

    employee_id = agent.employee_id

    response_noffers = client.get(f"/travelAgent/{employee_id}/offer")

    assert response_noffers.status_code == 400

    parsed_noffers = response_noffers.get_json()
    noffers_error = parsed_noffers["message"]

    assert noffers_error == "There are no Offers created by you"

    response_nagent = client.get("/travelAgent/432/offer")

    assert response_nagent.status_code == 400

    parsed_nagent = response_nagent.get_json()
    nagent_error = parsed_nagent["message"]

    assert nagent_error == "TravelAgent not found"






