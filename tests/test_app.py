from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    """Test GET /activities returns the activity data."""
    # Arrange: No special setup needed as activities are predefined

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0  # Ensure activities exist
    # Check a known activity
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success():
    """Test successful signup for an activity."""
    # Arrange
    email = "test@example.com"
    activity = "Programming Class"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify participant was added
    response_check = client.get("/activities")
    data_check = response_check.json()
    assert email in data_check[activity]["participants"]


def test_signup_duplicate():
    """Test that duplicate signup is rejected."""
    # Arrange
    email = "duplicate@example.com"
    activity = "Gym Class"

    # First signup
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act: Try to signup again
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_remove_participant_success():
    """Test successful removal of a participant."""
    # Arrange
    email = "remove@example.com"
    activity = "Basketball Team"

    # Add participant first
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify participant was removed
    response_check = client.get("/activities")
    data_check = response_check.json()
    assert email not in data_check[activity]["participants"]


def test_remove_participant_not_found():
    """Test removal of non-existent participant."""
    # Arrange
    email = "nonexistent@example.com"
    activity = "Tennis Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_remove_participant_invalid_activity():
    """Test removal from invalid activity."""
    # Arrange
    email = "test@example.com"
    activity = "Invalid Activity"

    # Act
    response = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]