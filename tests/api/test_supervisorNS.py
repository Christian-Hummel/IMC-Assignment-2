import pytest

from src.database import db
from tests.fixtures import app, client, agency

def test_add_supervisor(client,agency):

    response = client.post("/supervisor/", json={
        "name":"Warren Buffet",
        "address":"103 Avenue, 4932 New York",
        "salary": 20000,
        "nationality":"USA"
    })


    assert response.status_code == 200


    parsed = response.get_json()
    supervisor_response = parsed["supervisor"]


    assert supervisor_response["name"] == "Warren Buffet"
    assert supervisor_response["address"] == "103 Avenue, 4932 New York"
    assert supervisor_response["salary"] == 20000
    assert supervisor_response["nationality"] == "USA"
