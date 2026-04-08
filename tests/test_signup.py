"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up fixtures and test data
- Act: Call the endpoint
- Assert: Verify response status, message, and data state changes
"""

import pytest


class TestSignupForActivity:
    """Test suite for the signup endpoint"""

    def test_signup_with_valid_email_and_activity_succeeds(self, client, reset_activities):
        """
        Test that signup with valid email and existing activity returns 200.
        
        Arrange: Test client is ready, email is "test@mergington.edu", activity is "Chess Club"
        Act: POST to /activities/Chess Club/signup?email=test@mergington.edu
        Assert: Status code is 200
        """
        # Arrange
        email = "test@mergington.edu"
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_signup_returns_success_message(self, client, reset_activities):
        """
        Test that signup returns a success message.
        
        Arrange: Test client is ready
        Act: POST signup for test@mergington.edu for Programming Class
        Assert: Response contains success message
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Programming Class"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """
        Test that signup actually adds the participant to the activity.
        
        Arrange: Test client is ready
        Act: Sign up test@mergington.edu for Basketball Team, then fetch activities
        Assert: test@mergington.edu appears in Basketball Team participants
        """
        # Arrange
        email = "test@mergington.edu"
        activity = "Basketball Team"
        
        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email in activities[activity]["participants"]

    def test_signup_with_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Test that signup for non-existent activity returns 404.
        
        Arrange: Test client is ready
        Act: POST signup for non-existent activity "Fake Club"
        Assert: Status code is 404
        """
        # Arrange
        email = "test@mergington.edu"
        activity = "Fake Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_email_returns_400(self, client, reset_activities):
        """
        Test that signing up a student twice for same activity returns 400.
        
        Arrange: "michael@mergington.edu" is already in Chess Club
        Act: Try to sign up michael@mergington.edu for Chess Club again
        Assert: Status code is 400 and error message mentions already signed up
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_different_activities_same_email_succeeds(self, client, reset_activities):
        """
        Test that same email can sign up for multiple different activities.
        
        Arrange: Test client is ready, test@mergington.edu is not signed up for anything
        Act: Sign up test@mergington.edu for Chess Club and Programming Class
        Assert: Both sign-ups succeed and participant is in both activities
        """
        # Arrange
        email = "test@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]

    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """
        Test that multiple different students can sign up for the same activity.
        
        Arrange: Test client is ready
        Act: Sign up student1@mergington.edu and student2@mergington.edu for Tennis Club
        Assert: Both are added as participants
        """
        # Arrange
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        activity = "Tennis Club"
        
        # Act
        response1 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity]["participants"]
        assert email2 in activities[activity]["participants"]

    def test_signup_preserves_existing_participants(self, client, reset_activities):
        """
        Test that adding a new participant doesn't remove existing ones.
        
        Arrange: Chess Club has michael@mergington.edu and daniel@mergington.edu
        Act: Sign up newstudent@mergington.edu for Chess Club
        Assert: All three participants are present
        """
        # Arrange
        new_email = "newstudent@mergington.edu"
        activity = "Chess Club"
        existing_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act
        client.post(f"/activities/{activity}/signup", params={"email": new_email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for existing_email in existing_participants:
            assert existing_email in activities[activity]["participants"]
        assert new_email in activities[activity]["participants"]
        assert len(activities[activity]["participants"]) == 3
