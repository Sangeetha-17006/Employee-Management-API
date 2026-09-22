from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.core.exceptions import EmployeeManagementException

from app.models.department import Department

from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    existing_department = (
        db.query(Department)
        .filter(Department.name == department.name)
        .first()
    )

    if existing_department:
        raise EmployeeManagementException(
            message="Department with this name already exists",
            status_code=400
        )

    new_department = Department(
        name=department.name,
        description=department.description
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def get_departments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Department).all()


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not department:
        raise EmployeeManagementException(
            message="Department not found",
            status_code=404
        )

    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_department(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not department:
        raise EmployeeManagementException(
            message="Department not found",
            status_code=404
        )

    existing_department = (
        db.query(Department)
        .filter(
            Department.name == department_data.name,
            Department.id != department_id
        )
        .first()
    )

    if existing_department:
        raise EmployeeManagementException(
            message="Department with this name already exists",
            status_code=400
        )

    department.name = department_data.name
    department.description = department_data.description

    db.commit()
    db.refresh(department)

    return department


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if not department:
        raise EmployeeManagementException(
            message="Department not found",
            status_code=404
        )

    if department.employees:
        raise EmployeeManagementException(
            message="Cannot delete department with assigned employees",
            status_code=400
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }