from fastapi import FastAPI
import requests
from tutorial.tutorial_modules.tutorial_5_connect_wifi.wifi_enable import main as wifi_enable
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial.tutorial_modules.tutorial_6_send_wifi_commands.send_wifi_command import main as send_wifi_command
import sys
import asyncio
import argparse
from tutorial_modules import GOPRO_BASE_URL, logger
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import get_media_list
app = FastAPI()


@app.get("/connectCameras")
async def connect_to_cameras():
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera via BLE, get WiFi info, and enable WiFi."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default \
                camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        help="time in seconds to maintain connection before disconnecting. If not set, will maintain connection indefinitely",
        default=None,
    )
    args = parser.parse_args()
    try:
        asyncio.run(wifi_enable(args.identifier, args.timeout))
        return {"message": "Cameras connected"}

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        sys.exit(-1)


@ app.get("/record")
async def record():
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, set the shutter on, wait 2 seconds, then set the shutter off."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    try:
        send_wifi_command("/gopro/camera/setting?setting=167&option=2")
        asyncio.run(ble_command_set_shutter(args.identifier, [3, 1, 1, 1]))
        return {"message": "Record started"}

    except Exception as e:
        logger.error(e)
        sys.exit(-1)


@ app.get("/stopRecording")
async def stopRecording():
    parser = argparse.ArgumentParser(
        description="Connect to a GoPro camera, set the shutter on, wait 2 seconds, then set the shutter off."
    )
    parser.add_argument(
        "-i",
        "--identifier",
        type=str,
        help="Last 4 digits of GoPro serial number, which is the last 4 digits of the default camera SSID. If not used, first discovered GoPro will be connected to",
        default=None,
    )
    args = parser.parse_args()

    try:
        asyncio.run(ble_command_set_shutter(args.identifier, [3, 1, 1, 1]))
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
        sys.exit(-1)


@ app.get("/getBattery")
async def getBattery():
    return {"message": "Battery here :)"}
