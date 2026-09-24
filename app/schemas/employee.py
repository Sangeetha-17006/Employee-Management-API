from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department_id: int = Field(..., gt=0)
    position: str = Field(..., min_length=2, max_length=100)
    salary: float = Field(..., gt=0)


class EmployeeCreate(EmployeeBase):
    pass


class DepartmentSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class EmployeeResponse(EmployeeBase):
    id: int
    department: DepartmentSummary

    model_config = ConfigDict(from_attributes=True)