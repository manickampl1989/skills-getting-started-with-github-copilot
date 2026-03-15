import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def reset_activities():
    # Reset the in-memory activities dict to its initial state for test isolation
    for activity in activities.values():
        activity['participants'].clear()
    activities['Chess Club']['participants'].extend([
        "michael@mergington.edu", "daniel@mergington.edu"
    ])
    activities['Programming Class']['participants'].extend([
        "emma@mergington.edu", "sophia@mergington.edu"
    ])
    activities['Gym Class']['participants'].extend([
        "john@mergington.edu", "olivia@mergington.edu"
    ])
    activities['Soccer Team']['participants'].extend([
        "lucas@mergington.edu", "mia@mergington.edu"
    ])
    activities['Basketball Club']['participants'].extend([
        "liam@mergington.edu", "ava@mergington.edu"
    ])
    activities['Art Club']['participants'].extend([
        "noah@mergington.edu", "isabella@mergington.edu"
    ])
    activities['Drama Society']['participants'].extend([
        "ethan@mergington.edu", "charlotte@mergington.edu"
    ])
    activities['Math Olympiad']['participants'].extend([
        "amelia@mergington.edu", "jack@mergington.edu"
    ])
    activities['Science Club']['participants'].extend([
        "benjamin@mergington.edu", "harper@mergington.edu"
    ])

@pytest.fixture(autouse=True)
def setup_and_teardown():
    reset_activities()
    yield
    reset_activities()

def test_get_activities():
    # Arrange: None needed, uses default state
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_activity_not_found():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
