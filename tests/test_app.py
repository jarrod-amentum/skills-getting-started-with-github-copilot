from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed, uses in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure clean state
    client.get("/activities")  # Touch endpoint to initialize if needed
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"].startswith("Signed up")
    # Confirm student is now in participants
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"
