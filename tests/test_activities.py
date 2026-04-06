def test_get_activities_returns_all_activities(client, reset_activities):
    """Test that GET /activities returns all available activities
    
    Arrange: Define expected activity names
    Act: Send GET request to /activities endpoint
    Assert: Verify all expected activities are returned
    """
    # Arrange
    expected_activity_names = {
        "Chess Club", "Programming Class", "Gym Class", "Soccer Club",
        "Basketball League", "Art Club", "Drama Workshop", "Science Club", "Debate Team"
    }
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert set(activities.keys()) == expected_activity_names


def test_activity_has_required_fields(client, reset_activities):
    """Test that each activity has all required fields
    
    Arrange: Define required fields for activity objects
    Act: Send GET request to /activities endpoint
    Assert: Verify each activity contains all required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name, activity_data in activities.items():
        assert required_fields.issubset(set(activity_data.keys())), \
            f"Activity '{activity_name}' is missing required fields"
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_activities_have_participants(client, reset_activities):
    """Test that activities contain participant data
    
    Arrange: Use pre-loaded activities from app.py
    Act: Send GET request to /activities endpoint
    Assert: Verify at least one activity has participants
    """
    # Arrange
    # (participants are pre-loaded in app.py)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    # At least one activity should have participants
    assert any(len(activity["participants"]) > 0 for activity in activities.values())
