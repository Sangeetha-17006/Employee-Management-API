def get_admin_token(client, db):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "admin_test",
            "email": "admin_test@example.com",
            "password": "admin123456"
        }
    )

    assert response.status_code == 201

    from app.models.user import User

    user = (
        db.query(User)
        .filter(User.username == "admin_test")
        .first()
    )

    assert user is not None

    user.role = "admin"
    db.commit()

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "admin_test",
            "password": "admin123456"
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_create_employee(client, db):
    token = get_admin_token(client, db)

    # Create department first
    department_response = client.post(
        "/api/v1/departments/",
        json={
            "name": "Engineering",
            "description": "Software engineering department"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert department_response.status_code == 201

    department_id = department_response.json()["id"]

    # Create employee
    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Test Employee",
            "email": "employee@test.com",
            "department_id": department_id,
            "position": "Software Developer",
            "salary": 50000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Employee"
    assert data["email"] == "employee@test.com"
    assert data["position"] == "Software Developer"
    assert data["salary"] == 50000
    assert data["department"]["name"] == "Engineering"
