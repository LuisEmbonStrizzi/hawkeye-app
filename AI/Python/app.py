from fastapi import FastAPI
from pydantic import BaseModel
from speedtest import soFile
#from ball_tracking2 import tracking
app = FastAPI()

class Msg(BaseModel):
    url: str


@app.get("/")
async def speedtest():
    result = soFile()

    return {"result": result}


#@app.post("/predict")
#async def predict(inp: Msg):

    #pts_piques_finales = tracking(inp.url)

    #return {"piques_finales": pts_piques_finales}