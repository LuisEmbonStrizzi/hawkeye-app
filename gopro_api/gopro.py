from fastapi import FastAPI
from open_gopro import WirelessGoPro, Params
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

@app.get("/getVideo")
async def getVideo():
    return {"video": "https://res.cloudinary.com/dfpitoil1/video/upload/eo_10,so_6.5/v1681685906/fargowg6dr7m8wj9njcg.mp4", "message": "Hola"}

@app.get("/getBattery")
async def getBattery():
    return {"message": "Battery here :)"}

@app.get("/disconnectCameras")
async def disconnectCameras():
    with WirelessGoPro() as gopro:
        gopro.close()
    return {"message": "Cameras disconnected)"}