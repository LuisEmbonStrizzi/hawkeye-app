from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


class Msg(BaseModel):
    msg: str


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(inp: Msg):
    return {"message": inp.msg}
