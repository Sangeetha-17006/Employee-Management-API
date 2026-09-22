from pydantic import BaseModel, EmailStr, Field


# =========================
# USER REGISTRATION
# =========================

class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    username: str
    password: str


# =========================
# TOKEN RESPONSE
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str