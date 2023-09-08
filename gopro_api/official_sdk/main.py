from fastapi import FastAPI
import requests
from tutorial.tutorial_modules.tutorial_5_connect_wifi.wifi_enable import enable_wifi
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial.tutorial_modules.tutorial_6_send_wifi_commands.send_wifi_command import main as send_wifi_command
from tutorial_modules import GOPRO_BASE_URL, logger
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import get_media_list
app = FastAPI()


@app.get("/connectCameras")
async def connect_to_cameras():
    try:
        await enable_wifi()
        return {"message": "Camera connected"}

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)


@ app.get("/record")
async def record():
    try:
        send_wifi_command("/gopro/camera/setting?setting=167&option=2")
        await ble_command_set_shutter([3, 1, 1, 1])
        return {"message": "Record started"}

    except Exception as e:
        logger.error(e)


@ app.get("/stopRecording")
async def stopRecording():
    try:
        await ble_command_set_shutter([3, 1, 1, 0])
        media_list = get_media_list()
        video = [x["n"] for x in media_list["media"][0]["fs"]][-1]

        assert video is not None
    # Build the url to get the thumbnail data for the video
        logger.info(f"Downloading {video}")
        url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{video}"
        logger.info(f"Sending: {url}")
        with requests.get(url, stream=True, timeout=10) as request:
            request.raise_for_status()
            file = video.split(".")[0] + ".mp4"
        with open(file, "wb") as f:
            logger.info(f"receiving binary stream to {file}...")
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)

        return {"message": "Record stopped", "file": file}

    except Exception as e:
        logger.error(e)


@ app.get("/getBattery")
async def getBattery():
    return {"message": "Battery here :)"}
