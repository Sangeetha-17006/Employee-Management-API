def get_admin_token(client, db):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "department_admin",
            "email": "department_admin@example.com",
            "password": "admin123456"
        }
    )

    assert response.status_code == 201

    from app.models.user import User

    user = (
        db.query(User)
        .filter(User.username == "department_admin")
        .first()
    )

    assert user is not None

    user.role = "admin"
    db.commit()

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "department_admin",
            "password": "admin123456"
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_create_department(client, db):
    token = get_admin_token(client, db)

    response = client.post(
        "/api/v1/departments/",
        json={
            "name": "Finance",
            "description": "Finance and accounting department"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Finance"
    assert data["description"] == "Finance and accounting department"
    assert "id" in data


def test_get_departments(client, db):
    token = get_admin_token(client, db)

    client.post(
        "/api/v1/departments/",
        json={
            "name": "Human Resources",
            "description": "HR department"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/api/v1/departments/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Human Resources"


def test_duplicate_department(client, db):
    token = get_admin_token(client, db)

    department_data = {
        "name": "Operations",
        "description": "Operations department"
    }

    first_response = client.post(
        "/api/v1/departments/",
        json=department_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/departments/",
        json=department_data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["success"] is False
    assert data["error"] == "Department with this name already exists"