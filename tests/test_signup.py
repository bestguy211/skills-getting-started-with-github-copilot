def test_signup_successful(client, reset_activities):
    """Test successful signup for an activity
    
    Arrange: Define activity name and new student email
    Act: Send POST request to signup endpoint
    Assert: Verify response is successful with confirmation message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert email in response.json()["message"].lower()


def test_signup_adds_participant_to_list(client, reset_activities):
    """Test that signup adds participant to the activity's participants list
    
    Arrange: Define activity name and new student email
    Act: Register new participant and fetch updated activity data
    Assert: Verify participant appears in activity's participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act - Register new participant
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client, reset_activities):
    """Test signup fails when activity doesn't exist
    
    Arrange: Define non-existent activity name and student email
    Act: Send POST request to signup endpoint
    Assert: Verify 404 error response with appropriate message
    """
    # Arrange
    activity_name = "NonexistentActivity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_email_rejected(client, reset_activities):
    """Test signup fails when student already registered
    
    Arrange: Use email already registered for activity
    Act: Send POST request to signup endpoint with duplicate email
    Assert: Verify 400 error response indicating already signed up
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up in initial data
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
