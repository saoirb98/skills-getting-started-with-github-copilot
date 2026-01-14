import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate():
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    client.delete(f"/activities/{activity}/participants/{email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_nonexistent_participant():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/participants/someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
