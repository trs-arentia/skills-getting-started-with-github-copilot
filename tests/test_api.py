"""
API endpoint tests for Mergington High School Activities API
"""
import pytest


def test_get_activities(client):
	"""Test GET /activities endpoint returns all activities"""
	response = client.get("/activities")
	assert response.status_code == 200

	data = response.json()
	assert isinstance(data, dict)
	assert len(data) == 9  # We have 9 activities

	# Check that Chess Club exists with correct structure
	assert "Chess Club" in data
	assert "description" in data["Chess Club"]
	assert "schedule" in data["Chess Club"]
	assert "max_participants" in data["Chess Club"]
	assert "participants" in data["Chess Club"]
	assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success(client):
	"""Test successful participant signup"""
	response = client.post(
		"/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
	)
	assert response.status_code == 200

	data = response.json()
	assert "message" in data
	assert "newstudent@mergington.edu" in data["message"]
	assert "Chess Club" in data["message"]

	# Verify participant was added
	activities_response = client.get("/activities")
	activities = activities_response.json()
	assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate(client):
	"""Test that duplicate signup is prevented"""
	email = "michael@mergington.edu"  # Already in Chess Club

	response = client.post(
		f"/activities/Chess%20Club/signup?email={email}"
	)
	assert response.status_code == 400

	data = response.json()
	assert "detail" in data
	assert "already signed up" in data["detail"].lower()


def test_signup_invalid_activity(client):
	"""Test signup to non-existent activity returns 404"""
	response = client.post(
		"/activities/NonExistent%20Activity/signup?email=test@mergington.edu"
	)
	assert response.status_code == 404

	data = response.json()
	assert "detail" in data
	assert "not found" in data["detail"].lower()


def test_unregister_success(client):
	"""Test successful participant unregistration"""
	email = "michael@mergington.edu"  # Registered in Chess Club

	response = client.delete(
		f"/activities/Chess%20Club/unregister?email={email}"
	)
	assert response.status_code == 200

	data = response.json()
	assert "message" in data
	assert email in data["message"]
	assert "Chess Club" in data["message"]

	# Verify participant was removed
	activities_response = client.get("/activities")
	activities = activities_response.json()
	assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_registered(client):
	"""Test unregistering a non-registered participant returns 404"""
	response = client.delete(
		"/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
	)
	assert response.status_code == 404

	data = response.json()
	assert "detail" in data
	assert "not registered" in data["detail"].lower()


def test_unregister_invalid_activity(client):
	"""Test unregister from non-existent activity returns 404"""
	response = client.delete(
		"/activities/NonExistent%20Activity/unregister?email=test@mergington.edu"
	)
	assert response.status_code == 404

	data = response.json()
	assert "detail" in data
	assert "not found" in data["detail"].lower()


def test_signup_updates_participants_list(client):
	"""Test that signup correctly adds participant to the list"""
	activity_name = "Programming Class"
	email = "newcoder@mergington.edu"

	# Get initial participant count
	initial_response = client.get("/activities")
	initial_count = len(initial_response.json()[activity_name]["participants"])

	# Sign up new participant
	client.post(f"/activities/{activity_name.replace(' ', '%20')}/signup?email={email}")

	# Verify count increased
	final_response = client.get("/activities")
	final_activities = final_response.json()
	assert len(final_activities[activity_name]["participants"]) == initial_count + 1
	assert email in final_activities[activity_name]["participants"]


def test_unregister_removes_from_participants_list(client):
	"""Test that unregister correctly removes participant from the list"""
	activity_name = "Drama Club"
	email = "james@mergington.edu"  # Already registered

	# Get initial participant count
	initial_response = client.get("/activities")
	initial_count = len(initial_response.json()[activity_name]["participants"])

	# Unregister participant
	client.delete(f"/activities/{activity_name.replace(' ', '%20')}/unregister?email={email}")

	# Verify count decreased
	final_response = client.get("/activities")
	final_activities = final_response.json()
	assert len(final_activities[activity_name]["participants"]) == initial_count - 1
	assert email not in final_activities[activity_name]["participants"]


def test_multiple_signups_different_activities(client):
	"""Test that a student can sign up for multiple different activities"""
	email = "multitasker@mergington.edu"

	# Sign up for Chess Club
	response1 = client.post(f"/activities/Chess%20Club/signup?email={email}")
	assert response1.status_code == 200

	# Sign up for Swimming Club
	response2 = client.post(f"/activities/Swimming%20Club/signup?email={email}")
	assert response2.status_code == 200

	# Verify participant is in both
	activities_response = client.get("/activities")
	activities = activities_response.json()
	assert email in activities["Chess Club"]["participants"]
	assert email in activities["Swimming Club"]["participants"]


def test_activity_data_structure(client):
	"""Test that each activity has the correct data structure"""
	response = client.get("/activities")
	activities = response.json()

	required_fields = ["description", "schedule", "max_participants", "participants"]

	for activity_name, activity_data in activities.items():
		for field in required_fields:
			assert field in activity_data, f"{activity_name} missing {field}"

		assert isinstance(activity_data["description"], str)
		assert isinstance(activity_data["schedule"], str)
		assert isinstance(activity_data["max_participants"], int)
		assert isinstance(activity_data["participants"], list)
		assert activity_data["max_participants"] > 0
