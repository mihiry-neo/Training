from fastapi import FastAPI
from models import User
from responses import UserSummaryResponse

app = FastAPI(
    title="User Profile Summary API",
    description="A FastAPI Mini Project that returns a summary of User Data",
    version="1.0.0"
)

@app.get("/")
def root():
    return "Welcome to the User Info API"

@app.post("/user-info/", response_model=UserSummaryResponse)
def user_info(user:User):
    summary = {
        "Name":user.name,
        "Age":user.age,
        "Email":user.email,
        "Bio":user.bio or "No Bio Provided"
    }
    return {
        "message": f"Hi {user.name}, your profile was submitted successfully!",
        "details": summary
    }