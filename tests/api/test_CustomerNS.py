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
