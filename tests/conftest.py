"""
Pytest configuration and fixtures for the Mergington High School Activities API tests.

This module provides reusable fixtures for testing using the AAA (Arrange-Act-Assert) pattern:
- Arrange: Fixtures set up test data and test client
- Act: Test functions use the client to make API calls
- Assert: Test functions verify status codes and response data
"""

import pytest
from starlette.testclient import TestClient
from src.app import app, get_default_activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI application.
    
    This client is used to make test requests to the API without running a live server.
    Each test gets a fresh client instance.
    """
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """
    Fixture that provides fresh sample activity data for testing.
    
    Returns a deep copy of the default activities to ensure test isolation.
    Each test gets its own copy so modifications don't affect other tests.
    """
    import copy
    return copy.deepcopy(get_default_activities())


@pytest.fixture
def reset_activities(sample_activities):
    """
    Fixture that resets the app's activities to default state before each test.
    
    This ensures test isolation by clearing any modifications made during previous tests.
    Yields control to the test, then cleans up after.
    """
    from src.app import app as app_module
    import src.app
    
    # Store original activities
    original_activities = src.app.activities
    
    # Reset to fresh copy
    import copy
    src.app.activities = copy.deepcopy(get_default_activities())
    app_module.activities = src.app.activities
    
    yield
    
    # Restore after test
    src.app.activities = original_activities
    app_module.activities = original_activities
