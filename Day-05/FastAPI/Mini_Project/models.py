from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(...,ge=1,le=100, description="User's age must be between 1 and 100")
    email:EmailStr
    bio: str | None = None