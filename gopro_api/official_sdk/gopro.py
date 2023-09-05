from fastapi import FastAPI
from gopro_api import WirelessGoPro, Params
app = FastAPI()

@app.get("/connectCameras")
async def connect_to_cameras():
    with WirelessGoPro() as gopro:
        gopro.ble_command.set_shutter(Params.Toggle.ENABLE)
    return {"message": "Cameras connected"}

@app.get("/record")
async def record():
    with WirelessGoPro() as gopro:
        gopro.ble_command.set_shutter(Params.Toggle.ENABLE)
    return {"message": "Record started"}

@app.get("/stopRecording")
async def stopRecording():
    with WirelessGoPro() as gopro:
        gopro.ble_command.set_shutter(Params.Toggle.DISABLE)
    return {"message": "Record stopped"}

@app.get("/getBattery")
async def getBattery():
    return {"message": "Battery here :)"}

@app.get("/disconnectCameras")
async def disconnectCameras():
    with WirelessGoPro() as gopro:
        gopro.close()
    return {"message": "Cameras disconnected)"}
