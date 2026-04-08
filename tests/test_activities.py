"""
Tests for the GET /activities endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up fixtures and test client
- Act: Call the endpoint
- Assert: Verify response status, structure, and data
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint"""

    def test_get_activities_returns_success(self, client, reset_activities):
        """
        Test that GET /activities returns a 200 status code.
        
        Arrange: Test client is ready
        Act: Call GET /activities
        Assert: Status code is 200
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Test that GET /activities returns all 9 activities.
        
        Arrange: Test client is ready with default data
        Act: Call GET /activities
        Assert: Response contains 9 activities
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Theater Club",
            "Debate Team",
            "Science Club"
        ]
        assert list(activities.keys()) == expected_activities

    def test_get_activities_has_correct_structure(self, client, reset_activities):
        """
        Test that each activity has the required fields.
        
        Arrange: Test client is ready
        Act: Call GET /activities
        Assert: Each activity has description, schedule, max_participants, and participants
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        required_fields = {"description", "schedule", "max_participants", "participants"}
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_contains_correct_participant_data(self, client, reset_activities):
        """
        Test that activities contain the expected participants.
        
        Arrange: Test client is ready with default data
        Act: Call GET /activities
        Assert: Chess Club has michael@mergington.edu and daniel@mergington.edu
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club = activities["Chess Club"]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert len(chess_club["participants"]) == 2

    def test_get_activities_participants_are_email_strings(self, client, reset_activities):
        """
        Test that all participants are valid email strings.
        
        Arrange: Test client is ready
        Act: Call GET /activities
        Assert: All participants are strings and contain email format
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant
                assert participant.endswith(".edu")

    def test_get_activities_max_participants_is_positive(self, client, reset_activities):
        """
        Test that max_participants is positive for all activities.
        
        Arrange: Test client is ready
        Act: Call GET /activities
        Assert: All max_participants values are > 0
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] > 0
