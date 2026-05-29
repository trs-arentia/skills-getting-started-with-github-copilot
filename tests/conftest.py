"""
Pytest configuration and fixtures for API tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
	"""Create a test client for the FastAPI app"""
	return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
	"""Reset activities data before each test to ensure isolation"""
	# Save original activities
	original_activities = {
		"Chess Club": {
			"description": "Learn strategies and compete in chess tournaments",
			"schedule": "Fridays, 3:30 PM - 5:00 PM",
			"max_participants": 12,
			"participants": ["michael@mergington.edu", "daniel@mergington.edu"]
		},
		"Programming Class": {
			"description": "Learn programming fundamentals and build software projects",
			"schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
			"max_participants": 20,
			"participants": ["emma@mergington.edu", "sophia@mergington.edu"]
		},
		"Gym Class": {
			"description": "Physical education and sports activities",
			"schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
			"max_participants": 30,
			"participants": ["john@mergington.edu", "olivia@mergington.edu"]
		},
		"Soccer Team": {
			"description": "Join the school soccer team and compete in local tournaments",
			"schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
			"max_participants": 25,
			"participants": ["alex@mergington.edu", "lucas@mergington.edu"]
		},
		"Swimming Club": {
			"description": "Learn swimming techniques and train for competitions",
			"schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
			"max_participants": 15,
			"participants": ["sarah@mergington.edu"]
		},
		"Art Studio": {
			"description": "Explore painting, drawing, and sculpture techniques",
			"schedule": "Wednesdays, 3:30 PM - 5:00 PM",
			"max_participants": 18,
			"participants": ["emily@mergington.edu", "grace@mergington.edu"]
		},
		"Drama Club": {
			"description": "Develop acting skills and perform in school plays",
			"schedule": "Thursdays, 3:30 PM - 5:30 PM",
			"max_participants": 20,
			"participants": ["james@mergington.edu", "lily@mergington.edu", "noah@mergington.edu"]
		},
		"Debate Team": {
			"description": "Improve critical thinking and public speaking through debates",
			"schedule": "Fridays, 3:00 PM - 4:30 PM",
			"max_participants": 16,
			"participants": ["oliver@mergington.edu", "ava@mergington.edu"]
		},
		"Science Club": {
			"description": "Conduct experiments and participate in science fairs",
			"schedule": "Tuesdays, 3:30 PM - 5:00 PM",
			"max_participants": 14,
			"participants": ["william@mergington.edu", "isabella@mergington.edu"]
		}
	}

	# Reset activities before test
	activities.clear()
	activities.update(original_activities)

	yield

	# Reset activities after test
	activities.clear()
	activities.update(original_activities)
