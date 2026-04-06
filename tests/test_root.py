def test_root_redirects_to_static(client):
    """Test that root endpoint redirects to static/index.html
    
    Arrange: Use the client fixture
    Act: Send GET request to root endpoint
    Assert: Verify redirect status and location
    """
    # Arrange
    # (setup is implicit in client fixture)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
