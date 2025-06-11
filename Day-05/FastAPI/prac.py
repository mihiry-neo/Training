from fastapi import FastAPI
from prac_models import User

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to FastAPI"}

@app.get("/hello/{name}")
def say_hello(name: str, greet: str = "Hello"):
    return {"greeting": f"{greet}, {name}!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.post("/submit")
def submit_data(data:User):
    return {"received": data.model_dump()}

# Pydantic model ensures that request validation happens as it checks whether the type is correct, all the fields are present, etc
# http://127.0.0.1:8000/hello/Mihir?greet=Hola Here, Mihir (name) is the path parameter and after ? greet is the Query Parameter
# http://127.0.0.1:8000/items/30?q=Iphone Here, 30 (item_id) is the path parameter and after ? q is the query parameter


@app.post("/user-info/")
def user_info(user: User):
    return {
        "message": f"Hi {user.name}, your email is {user.email} and you're {user.age} years old."
    }
