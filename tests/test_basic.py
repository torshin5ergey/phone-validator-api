
import os
import signal
import time
import json

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
    phones = "+7 (912) 783 2348"
    response = client.post(
        "/validatePhoneNumber",
        data=phones,
        content_type="text/plain"
    )

    assert response.status_code == 200
    response_data = json.loads(response.get_data(as_text=True))
    assert response_data.get("status") is True
    assert response_data.get("normalized") == "+7-912-783-2348"

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
