from fastapi import FastAPI
from pydantic import BaseModel
from ball_tracking2_cpp import tracking
app = FastAPI()


@app.get("/cv-api/")
def test():
    return {"message": "Hello World"}


class Msg(BaseModel):
    url: str


@app.post("/cv-api/predict")
async def predict(inp: Msg):

    pts_piques_finales = tracking(inp.url)

    return {"piques_finales": pts_piques_finales}
