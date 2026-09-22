Employee Management API



A production-style REST API for managing employees, departments, authentication, and role-based access control.



Features

Employee CRUD operations

Department management

JWT-based authentication

Role-based authorization

Admin and employee roles

Password hashing with bcrypt

Request validation with Pydantic

Search employees by name

Filter employees by department

Pagination support

Centralized application error handling

SQLite database with SQLAlchemy ORM

API versioning with /api/v1

Interactive Swagger/OpenAPI documentation

Tech Stack

Python 3.12

FastAPI

SQLAlchemy

Pydantic

SQLite

JWT

Passlib

bcrypt

Uvicorn

Swagger / OpenAPI

Project Structure

Employee-Management-API/

|

+-- app/

|   |

|   +-- core/

|   |   +-- config.py

|   |   +-- database.py

|   |   +-- exceptions.py

|   |   +-- security.py

|   |

|   +-- models/

|   |   +-- department.py

|   |   +-- employee.py

|   |   +-- user.py

|   |

|   +-- routers/

|   |   +-- auth.py

|   |   +-- department.py

|   |   +-- employee.py

|   |

|   +-- schemas/

|   |   +-- auth.py

|   |   +-- department.py

|   |   +-- employee.py

|   |

|   +-- services/

|   |

|   +-- main.py

|

+-- tests/

|

+-- .gitignore

+-- README.md

Installation



Clone the repository:



git clone <your-github-repository-url>

cd Employee-Management-API



Create a virtual environment:



py -3.12 -m venv .venv



Activate the virtual environment on Windows:



.venv\\Scripts\\activate



Install the required packages:



pip install -r requirements.txt

Environment Configuration



Create a .env file in the project root:



SECRET\_KEY=your-secret-key



The .env file should not be committed to GitHub.



Running the API



Start the FastAPI application with:



uvicorn app.main:app --reload



The API will be available at:



http://127.0.0.1:8000

API Documentation



Swagger UI:



http://127.0.0.1:8000/docs



ReDoc:



http://127.0.0.1:8000/redoc

Authentication



The API uses JWT-based authentication.



Register User

POST /api/v1/auth/register



Example request:



{

&#x20;   "username": "employee1",

&#x20;   "email": "employee1@example.com",

&#x20;   "password": "employee123"

}

Login

POST /api/v1/auth/login



The login endpoint returns an access token that can be used to access protected API endpoints.



User Roles



The application supports role-based access control.



Admin



Administrators can:



Create employees

Update employees

Delete employees

Create departments

Update departments

Delete departments

View employees

View departments

Employee



Employees can:



View employee information

View department information



Administrative operations require an authenticated administrator account.



Employee Endpoints

Method	Endpoint	Description

POST	/api/v1/employees/	Create employee

GET	/api/v1/employees/	List employees

GET	/api/v1/employees/{employee\_id}	Get employee

PUT	/api/v1/employees/{employee\_id}	Update employee

DELETE	/api/v1/employees/{employee\_id}	Delete employee

Department Endpoints

Method	Endpoint	Description

POST	/api/v1/departments/	Create department

GET	/api/v1/departments/	List departments

GET	/api/v1/departments/{department\_id}	Get department

PUT	/api/v1/departments/{department\_id}	Update department

DELETE	/api/v1/departments/{department\_id}	Delete department

Search, Filtering and Pagination



The employee listing endpoint supports searching, filtering, and pagination.



Example:



GET /api/v1/employees/?name=Rahul



Filter by department:



GET /api/v1/employees/?department\_id=1



Pagination:



GET /api/v1/employees/?page=1\&limit=10



Multiple parameters can be combined:



GET /api/v1/employees/?name=Rahul\&department\_id=1\&page=1\&limit=10

Validation



Request data is validated using Pydantic.



Examples of validation include:



Employee name length

Valid email format

Positive department ID

Valid position

Positive salary

Username length

Password length

Department name length



Invalid requests return HTTP 422 validation responses.



Error Handling



The application includes centralized custom exception handling.



Examples include:



Employee not found

Department not found

Duplicate employee email

Duplicate department name

Invalid credentials

Unauthorized access

Invalid pagination parameters

Database



The application uses:



SQLite for database storage

SQLAlchemy ORM for database operations

Relational relationships between employees and departments



The main database entities are:



Users

Employees

Departments

Security



Security features include:



JWT access tokens

Password hashing with bcrypt

Protected API endpoints

Role-based authorization

Environment-based secret configuration

Authentication validation

API Versioning



The application uses versioned API routes:



/api/v1/



This structure makes it possible to introduce future API versions without breaking existing clients.



Health Check



The API provides a health-check endpoint:



GET /health



Example response:



{

&#x20;   "status": "healthy"

}

Testing



The API can be tested using:



Swagger UI

Postman

Pytest



The project includes testing support for authentication, employee management, validation, authorization, and error handling.



Project Objective



The objective of this project is to demonstrate the development of a secure, modular, and scalable REST API using modern Python backend technologies.



The project covers real-world backend development concepts including:



REST API development

Database design

ORM-based data access

Authentication

Authorization

Data validation

Error handling

API versioning

Search and pagination

API documentation

Author



Sangeetha S

