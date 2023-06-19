from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
from speedtest import soFile
from ball_tracking2 import tracking
app = FastAPI()


class Msg(BaseModel):
    url: str


@app.get("/")
async def speedtest():
    subprocess.run(
        [
            "g++",
            "-fPIC",
            "-shared",
            "-o",
            "./cpplibrary.so",
            "./main.cpp",
            "-I/usr/include/opencv4",
            "-lopencv_core",
            "-lopencv_highgui",
            "-lopencv_imgcodecs",
            "-lopencv_imgproc",
        ]
    )

    result = soFile()

    return {"result": result}


@app.post("/predict")
async def predict(inp: Msg):

    pts_piques_finales = tracking(inp.url)

    return {"piques_finales": pts_piques_finales}
