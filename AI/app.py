from fastapi import FastAPI
from pydantic import BaseModel
from ball_tracking2 import tracking
app = FastAPI()

class Msg(BaseModel):
    msg: str
    url : str


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(inp: Msg):
    pts_piques_finales = tracking(inp.url)


    return {"message": pts_piques_finales}
