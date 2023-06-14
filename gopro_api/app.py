from fastapi import FastAPI
from gopro_api import gopro
app = FastAPI()

@app.get("/connectCameras")
async def connect_to_cameras():
    return {"message": "Cameras connected"}

@app.get("/record")
async def record():
    return {"message": "Record started"}

@app.get("/stopRecording")
async def stopRecording():
    return {"message": "Record stopped"}

@app.get("/getBattery")
async def stopRecording():
    return {"message": "Battery here :)"}
