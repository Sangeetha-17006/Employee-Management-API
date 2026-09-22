from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import Base, engine
from app.core.exceptions import EmployeeManagementException

from app.models.employee import Employee
from app.models.department import Department
from app.models.user import User

from app.routers.employee import router as employee_router
from app.routers.department import router as department_router
from app.routers.auth import router as auth_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    description="REST API for managing employees and HR data",
    version="1.0.0"
)


# =========================
# CUSTOM EXCEPTION HANDLER
# =========================
@app.exception_handler(EmployeeManagementException)
async def employee_management_exception_handler(
    request: Request,
    exc: EmployeeManagementException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message
        }
    )


# =========================
# ROUTERS
# =========================
app.include_router(
    employee_router,
    prefix="/api/v1"
)

app.include_router(
    department_router,
    prefix="/api/v1"
)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "Employee Management API is running"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }