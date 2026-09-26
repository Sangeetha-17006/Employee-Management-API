from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import EmployeeManagementException
from app.core.security import get_current_user, require_admin
from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeResponse


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# =========================
# CREATE EMPLOYEE
# =========================

@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    department = (
        db.query(Department)
        .filter(Department.id == employee.department_id)
        .first()
    )

    if department is None:
        raise EmployeeManagementException(
            message="Department not found",
            status_code=404
        )

    existing_employee = (
        db.query(Employee)
        .filter(Employee.email == employee.email)
        .first()
    )

    if existing_employee:
        raise EmployeeManagementException(
            message="Employee with this email already exists",
            status_code=400
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        department_id=employee.department_id,
        position=employee.position,
        salary=employee.salary
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# =========================
# GET EMPLOYEES
# SEARCH + FILTER + PAGINATION
# =========================

@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_employees(
    name: str | None = None,
    department_id: int | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if page < 1:
        raise EmployeeManagementException(
            message="Page must be greater than or equal to 1",
            status_code=400
        )

    if limit < 1 or limit > 100:
        raise EmployeeManagementException(
            message="Limit must be between 1 and 100",
            status_code=400
        )

    query = db.query(Employee)

    # Search by employee name
    if name:
        query = query.filter(
            Employee.name.ilike(f"%{name}%")
        )

    # Filter by department
    if department_id is not None:
        query = query.filter(
            Employee.department_id == department_id
        )

    # Pagination
    offset = (page - 1) * limit

    employees = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return employees


# =========================
# GET EMPLOYEE BY ID
# =========================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise EmployeeManagementException(
            message="Employee not found",
            status_code=404
        )

    return employee


# =========================
# UPDATE EMPLOYEE
# =========================

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise EmployeeManagementException(
            message="Employee not found",
            status_code=404
        )

    department = (
        db.query(Department)
        .filter(Department.id == employee_data.department_id)
        .first()
    )

    if department is None:
        raise EmployeeManagementException(
            message="Department not found",
            status_code=404
        )

    existing_employee = (
        db.query(Employee)
        .filter(
            Employee.email == employee_data.email,
            Employee.id != employee_id
        )
        .first()
    )

    if existing_employee:
        raise EmployeeManagementException(
            message="Employee with this email already exists",
            status_code=400
        )

    employee.name = employee_data.name
    employee.email = employee_data.email
    employee.department_id = employee_data.department_id
    employee.position = employee_data.position
    employee.salary = employee_data.salary

    db.commit()
    db.refresh(employee)

    return employee


# =========================
# DELETE EMPLOYEE
# =========================

@router.delete(
    "/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise EmployeeManagementException(
            message="Employee not found",
            status_code=404
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }