from fastapi import FastAPI
import time
import requests
from tutorial.tutorial_modules.tutorial_5_connect_wifi.wifi_enable import enable_wifi
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_load_group import main as ble_command_load_group
from tutorial.tutorial_modules.tutorial_6_send_wifi_commands.send_wifi_command import main as send_wifi_command
from tutorial_modules import GOPRO_BASE_URL, logger
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import get_media_list
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_state import main as get_camera_state
from azure.storage.blob import BlobServiceClient
import os
from decouple import config

app = FastAPI()

azure_connection_string = config('AZURE_CONNECTION_STRING')
container_name = config('AZURE_CONTAINER_NAME')


@app.get("/connectCameras")
async def connect_to_cameras():
    try:
        await enable_wifi()
        await ble_command_load_group(0x04, 0x3E, 0x02, 0x03, 0xE9)
        await ble_command_set_shutter([3, 1, 1, 1])
        media_list = get_media_list()
        foto = [x["n"] for x in media_list["media"][0]["fs"]][-1]

        assert foto is not None
    # Build the url to get the thumbnail data for the foto
        logger.info(f"Downloading {foto}")
        url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{foto}"
        logger.info(f"Sending: {url}")
        with requests.get(url, stream=True, timeout=10) as request:
            request.raise_for_status()
            file = foto.split(".")[0] + ".jpg"
        with open(file, "wb") as f:
            logger.info(f"receiving binary stream to {file}...")
            for chunk in request.iter_content(chunk_size=8192):
                f.write(chunk)

        blob_service_client = BlobServiceClient.from_connection_string(
            azure_connection_string)
        container_client = blob_service_client.get_container_client(
            container_name)
        # Nombre del archivo en Azure será el mismo que local
        blob_name = os.path.basename(file)
        blob_client = container_client.get_blob_client(blob_name)

        with open(file, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)

        # Obtener la URL del blob
        blob_url = blob_client.url

        return {"message": "Camera connected", "file_url": blob_url}

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

        blob_service_client = BlobServiceClient.from_connection_string(
            azure_connection_string)
        container_client = blob_service_client.get_container_client(
            container_name)
        # Nombre del archivo en Azure será el mismo que local
        blob_name = os.path.basename(file)
        blob_client = container_client.get_blob_client(blob_name)

        with open(file, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)

        # Obtener la URL del blob
        blob_url = blob_client.url

        return {"message": "Record stopped", "file_url": blob_url}

    except Exception as e:
        logger.error(e)


@ app.get("/getBattery")
async def getBattery():

    response = get_camera_state()
    data = response.json()
    return {"message": "Battery here :)", "battery": data["status"]["70"]}
