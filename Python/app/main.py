from fastapi import FastAPI
from pydantic import BaseModel

from calculator.calculator import calculate


app = FastAPI()


class Calculation(BaseModel):
    num1: str
    num2: str
    operator: str


@app.post("/api/calculator")
def calculator(data: Calculation):
    try:
        result = calculate(data.num1, data.num2, data.operator)
        return {"result": result}
    except ValueError as error:
        return {"error": str(error)}