import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True # enable flask test mode
    with app.test_client() as client: # create test client
        yield client

def test_root(client):
    # GET to url "/"
    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "hello world\n"
    assert "text/html" in response.content_type

def test_nonexists(client):
    response = client.get("/nonexists")

    assert response.status_code == 404
