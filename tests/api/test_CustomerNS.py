import pytest

from src.database import Supervisor, TravelAgent, Customer, Offer, Country, Activity, User, db

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


def test_request_expert(client,agency):

    customer = db.session.query(Customer).filter_by(customer_id=713).first()

    customer_id = customer.customer_id

    response = client.post(f"/customer/{customer_id}/expert")

    assert response.status_code == 200

    parsed = response.get_json()

    assert parsed == "You have requested to be assisted by an expert of France"


def test_request_expert_errors(client,agency):

    response_unregistered = client.post("/customer/524/expert")

    assert response_unregistered.status_code == 400

    parsed_unregistered = response_unregistered.get_json()
    unregistered_error = parsed_unregistered["message"]

    assert unregistered_error == "Customer not found"

    customer = db.session.query(Customer).filter_by(customer_id=706).first()

    customer_id = customer.customer_id

    response_expert = client.post(f"/customer/{customer_id}/expert")

    assert response_expert.status_code == 400

    parsed_expert = response_expert.get_json()
    expert_error = parsed_expert["message"]

    assert expert_error == "You have already requested an expert"

def test_show_offers(client,agency):

    customer = db.session.query(Customer).filter_by(customer_id=713).first()
    customer_id = customer.customer_id

    response = client.get(f"/customer/{customer_id}/offers")

    assert response.status_code == 200

    parsed = response.get_json()
    offers_response = parsed["offers"]

    assert len(offers_response) == 1

def test_show_offers_errors(client,agency):

    customer = db.session.query(Customer).filter_by(customer_id=703).first()
    customer_id = customer.customer_id

    response_noffers = client.get(f"/customer/{customer_id}/offers")

    assert response_noffers.status_code == 400

    parsed_noffer = response_noffers.get_json()
    noffer_error = parsed_noffer["message"]

    assert noffer_error == "There are no current offers"

    response_ncustomer = client.get(f"/customer/439/offers")

    assert response_ncustomer.status_code == 400

    parsed_ncustomer = response_ncustomer.get_json()
    ncustomer_error = parsed_ncustomer["message"]

    assert ncustomer_error == "Customer not found"


def test_handle_offer(client,agency):

    customer = db.session.query(Customer).filter_by(customer_id=709).first()

    customer_id = customer.customer_id

    offer1 = db.session.query(Offer).filter_by(offer_id=804).first()
    offer2 = db.session.query(Offer).filter_by(offer_id=813).first()
    offer3 = db.session.query(Offer).filter_by(offer_id=814).first()

    offer_id1 = offer1.offer_id
    offer_id2 = offer2.offer_id
    offer_id3 = offer3.offer_id

    response_accept = client.post(f"/customer/{customer_id}/offer/{offer_id1}", json={
        "input": "accept"
    })

    assert response_accept.status_code == 200

    message1 = response_accept.get_json()

    assert message1 == "Your trip to Scotland has been accepted, Thank you for choosing hammertrips"
    assert offer1.status == "accepted"

    response_change = client.post(f"/customer/{customer_id}/offer/{offer_id2}", json={
        "input": "change"
    })

    assert response_change.status_code == 200

    message2 = response_change.get_json()

    assert message2 == "Request send to TravelAgent to improve this offer"

    response_decline = client.post(f"/customer/{customer_id}/offer/{offer_id3}", json={
        "input": "decline"
    })

    assert response_decline.status_code == 200

    message3 = response_decline.get_json()

    assert message3 == "This trip has been cancelled"


def test_handle_offer_errors(client,agency):

    offer1 = db.session.query(Offer).filter_by(offer_id=809).first()

    offer_id1 = offer1.offer_id

    offer2 = db.session.query(Offer).filter_by(offer_id=813).first()

    offer_id2 = offer2.offer_id

    customer = db.session.query(Customer).filter_by(customer_id=709).first()

    customer_id = customer.customer_id

    response_noffer1 = client.post(f"/customer/{customer_id}/offer/583",json={
        "input": "accept"
    })

    assert response_noffer1.status_code == 400

    parsed_noffer1 = response_noffer1.get_json()
    noffer_error1 = parsed_noffer1["message"]

    assert noffer_error1 == "Offer not found"

    response_noffer2 = client.post(f"/customer/{customer_id}/offer/802", json={
        "input": "accept"
    })

    assert response_noffer1.status_code == 400

    parsed_noffer2 = response_noffer2.get_json()
    noffer_error2 = parsed_noffer2["message"]

    assert noffer_error2 == "Offer not found"

    response_ncustomer = client.post(f"/customer/429/offer/{offer_id1}", json={
        "input": "accept"
    })

    assert response_ncustomer.status_code == 400

    parsed_ncustomer = response_ncustomer.get_json()
    ncustomer_error = parsed_ncustomer["message"]

    assert ncustomer_error == "Customer not found"

    response_winput = client.post(f"/customer/{customer_id}/offer/{offer_id2}", json={
        "input": "cancel"
    })

    assert response_winput.status_code == 400

    parsed_winput = response_winput.get_json()
    winput_error = parsed_winput["message"]

    assert winput_error == "Please insert accept, change or decline to react to this offer"