def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully"
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "employee"


def test_login_user(client):
    # Register user first
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "testpassword123"
        }
    )

    assert register_response.status_code == 201

    # Login using OAuth2 form data
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "loginuser",
            "password": "testpassword123"
        }
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Invalid username or password"