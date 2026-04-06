def test_unregister_successful(client, reset_activities):
    """Test successful unregister from an activity
    
    Arrange: Use participant already registered for activity
    Act: Send DELETE request to unregister endpoint
    Assert: Verify response is successful with confirmation message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()


def test_unregister_removes_participant(client, reset_activities):
    """Test that unregister removes participant from activity
    
    Arrange: Use participant already registered for activity
    Act: Unregister participant and fetch updated activity data
    Assert: Verify participant no longer appears in activity's participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act - Unregister
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client, reset_activities):
    """Test unregister fails when activity doesn't exist
    
    Arrange: Define non-existent activity name and student email
    Act: Send DELETE request to unregister endpoint
    Assert: Verify 404 error response with appropriate message
    """
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_email_not_signed_up(client, reset_activities):
    """Test unregister fails when student is not registered
    
    Arrange: Define activity name and email not registered for activity
    Act: Send DELETE request to unregister endpoint
    Assert: Verify 400 error response indicating student not signed up
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()
