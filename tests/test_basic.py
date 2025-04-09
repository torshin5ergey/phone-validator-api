
import os
import signal
import time
import json
import random
from http import HTTPStatus

from unittest.mock import patch
import pytest
from faker import Faker

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True # enable flask test mode
    with app.test_client() as client: # create test client
        yield client

def test_ping(client):
    # GET to url "/"
    response = client.get("/ping")

    assert response.status_code == HTTPStatus.OK.value
    assert response.data.decode("utf-8") == "pong"
    assert "text/html" in response.content_type

def test_nonexists(client):
    response = client.get("/validatephonenumber")

    assert response.status_code == HTTPStatus.NOT_FOUND.value

def test_shutdown(client):
    # замена реального os.kill на мок объект
    with patch("os.kill") as mock_kill:
        response = client.get("/shutdown")

        assert response.status_code == HTTPStatus.OK.value
        assert response.data.decode("utf-8") == "Shutting down..."
        assert "text/html" in response.content_type
        time.sleep(1.5)
        # assert_called_once_with функция вызвана один раз с аргементами
        mock_kill.assert_called_once_with(os.getpid(), signal.SIGTERM)

def test_validate_phone_number_success(client):
    # Generate phone
    CODES = [982, 986, 912, 934]
    code = str(random.choice(CODES))
    mid = str(random.randint(0, 999))
    last = str(random.randint(0, 9999))
    TEMPLATES = (
        f"+7 {code} {mid.rjust(3, '0')} {last.rjust(4, '0')}",
        f"+7 ({code}) {mid.rjust(3, '0')} {last.rjust(4, '0')}",
        f"+7{code}{mid.rjust(3, '0')}{last.rjust(4, '0')}",
        f"8({code}){mid.rjust(3, '0')}-{last.rjust(4, '0')}",
        f"8{code}{mid.rjust(3, '0')}{last.rjust(4, '0')}"
    )
    NORMALIZED = f"+7-{code}-{mid.rjust(3, '0')}-{last.rjust(4, '0')}"

    # Test set
    for template in TEMPLATES:
        response = client.post(
            "/validatePhoneNumber",
            json={"phone_number": template},
            content_type="application/json"
        )
        assert response.status_code == HTTPStatus.OK.value
        response_data = response.get_json()
        assert response_data.get("status") is True
        assert response_data.get("normalized") == NORMALIZED

def test_validate_phone_number_br(client):
    """400 Bad Request"""
    # Generate phone
    fake = Faker("ru_RU")
    phone = fake.phone_number()

    response = client.post(
        "/validatePhoneNumber",
        json={"phone": phone},
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST.value

def test_validate_phone_number_nf(client):
    """404 Not Found"""
    # Generate phone
    fake = Faker("ru_RU")
    phone = fake.phone_number()

    response = client.post(
        "/validatePhoneNumber",
        json={"phone_number": phone},
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND.value
