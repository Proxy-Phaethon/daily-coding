from fastapi import FastAPI
from calculator import calculate

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Python Daily API is alive!"}