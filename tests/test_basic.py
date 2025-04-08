
import os
import signal
import time
import json
import random

from unittest.mock import patch
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True # enable flask test mode
    with app.test_client() as client: # create test client
        yield client

def test_ping(client):
    # GET to url "/"
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "pong"
    assert "text/html" in response.content_type

def test_nonexists(client):
    response = client.get("/nonexists")

    assert response.status_code == 404

def test_shutdown(client):
    # замена реального os.kill на мок объект
    with patch("os.kill") as mock_kill:
        response = client.get("/shutdown")

        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Shutting down..."
        assert "text/html" in response.content_type
        time.sleep(1.5)
        # assert_called_once_with функция вызвана один раз с аргементами
        mock_kill.assert_called_once_with(os.getpid(), signal.SIGTERM)

def test_validate_phone_number_success(client):
    CODES = [982, 986, 912, 934]
    # Generate phone
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
    print(TEMPLATES)
    NORMALIZED = f"+7-{code}-{mid.rjust(3, '0')}-{last.rjust(4, '0')}"
    print(NORMALIZED)
    for template in TEMPLATES:
        response = client.post(
            "/validatePhoneNumber",
            data=template,
            content_type="text/plain"
        )

        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert response_data.get("status") is True
        assert response_data.get("normalized") == NORMALIZED

def test_validate_phone_number_fail(client):
    phones = "+7 (912) 783 238"
    response = client.post(
        "/validatePhoneNumber",
        data=phones,
        content_type="text/plain"
    )

    assert response.status_code == 404
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get("status") is False
