from fastapi import FastAPI
from pydantic import BaseModel
from ball_tracking2_cpp import tracking
app = FastAPI()


class Msg(BaseModel):
    url: str


@app.post("/predict")
async def predict(inp: Msg):

    pts_piques_finales = tracking(inp.url)

    return {"piques_finales": pts_piques_finales}
