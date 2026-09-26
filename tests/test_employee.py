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


def get_employee_token(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "employee_test",
            "email": "employee_test@example.com",
            "password": "employee123"
        }
    )

    assert response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "employee_test",
            "password": "employee123"
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def create_test_department(client, token):
    response = client.post(
        "/api/v1/departments/",
        json={
            "name": "Engineering",
            "description": "Software engineering department"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_test_employee(client, token, department_id):
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

    return response.json()["id"]


def test_create_employee(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Test Employee",
            "email": "employee@test.com",
            "department_id": department_id,
            "position": "Software Developer",
            "salary": 50000
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Employee"
    assert data["email"] == "employee@test.com"
    assert data["position"] == "Software Developer"
    assert data["salary"] == 50000
    assert data["department"]["name"] == "Engineering"


def test_update_employee(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    employee_id = create_test_employee(
        client,
        token,
        department_id
    )

    response = client.put(
        f"/api/v1/employees/{employee_id}",
        json={
            "name": "Updated Employee",
            "email": "updated@test.com",
            "department_id": department_id,
            "position": "Senior Software Developer",
            "salary": 65000
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Employee"
    assert data["email"] == "updated@test.com"
    assert data["position"] == "Senior Software Developer"
    assert data["salary"] == 65000


def test_delete_employee(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    employee_id = create_test_employee(
        client,
        token,
        department_id
    )

    response = client.delete(
        f"/api/v1/employees/{employee_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Employee deleted successfully"


def test_employee_cannot_create_employee(client, db):
    admin_token = get_admin_token(client, db)

    department_id = create_test_department(
        client,
        admin_token
    )

    employee_token = get_employee_token(client)

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Unauthorized Employee",
            "email": "unauthorized@test.com",
            "department_id": department_id,
            "position": "Developer",
            "salary": 40000
        },
        headers={
            "Authorization": f"Bearer {employee_token}"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Admin access required"


def test_get_nonexistent_employee(client, db):
    token = get_admin_token(client, db)

    response = client.get(
        "/api/v1/employees/99999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Employee not found"


def test_create_employee_with_invalid_department(client, db):
    token = get_admin_token(client, db)

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Invalid Department Employee",
            "email": "invaliddepartment@test.com",
            "department_id": 99999,
            "position": "Developer",
            "salary": 50000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Department not found"


def test_search_employees_by_name(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    create_test_employee(
        client,
        token,
        department_id
    )

    response = client.get(
        "/api/v1/employees/?name=Test&page=1&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test Employee"


def test_filter_employees_by_department(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    create_test_employee(
        client,
        token,
        department_id
    )

    response = client.get(
        f"/api/v1/employees/?department_id={department_id}&page=1&limit=10",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["department_id"] == department_id


def test_employee_pagination(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    create_test_employee(
        client,
        token,
        department_id
    )

    response = client.get(
        "/api/v1/employees/?page=1&limit=1",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1


# =========================
# VALIDATION / ERROR TESTS
# =========================

def test_create_employee_with_invalid_email(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Invalid Email Employee",
            "email": "invalid-email",
            "department_id": department_id,
            "position": "Developer",
            "salary": 50000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422


def test_create_employee_with_negative_salary(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Invalid Salary Employee",
            "email": "invalidsalary@test.com",
            "department_id": department_id,
            "position": "Developer",
            "salary": -5000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422


def test_employee_pagination_invalid_limit(client, db):
    token = get_admin_token(client, db)

    response = client.get(
        "/api/v1/employees/?page=1&limit=101",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Limit must be between 1 and 100"


def test_duplicate_employee_email(client, db):
    token = get_admin_token(client, db)
    department_id = create_test_department(client, token)

    create_test_employee(
        client,
        token,
        department_id
    )

    response = client.post(
        "/api/v1/employees/",
        json={
            "name": "Duplicate Email Employee",
            "email": "employee@test.com",
            "department_id": department_id,
            "position": "Developer",
            "salary": 55000
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"] == "Employee with this email already exists"