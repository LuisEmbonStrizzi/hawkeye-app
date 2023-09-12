from typing import Optional
from fastapi import FastAPI
import time
import requests
from tutorial.tutorial_modules.tutorial_5_connect_wifi.wifi_enable import enable_wifi
from tutorial.tutorial_modules.tutorial_1_connect_ble.ble_connect import connect_ble
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_load_group import main as ble_command_load_group
from tutorial.tutorial_modules.tutorial_6_send_wifi_commands.send_wifi_command import main as send_wifi_command
from tutorial_modules import GOPRO_BASE_URL, logger, GOPRO_BASE_UUID
import asyncio
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import get_media_list
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_state import main as get_camera_state
from azure.storage.blob import BlobServiceClient
import os
from decouple import config
from bleak import BleakClient

app = FastAPI()

azure_connection_string = config('AZURE_CONNECTION_STRING')
container_name = config('AZURE_CONTAINER_NAME')
class BleClientManager:
    def __init__(self):
        self.ble_client: BleakClient = None

    def set_client(self, client: BleakClient):
        self.ble_client = client

    # Agregar métodos que deleguen a los métodos del objeto client
    def connect(self):
        if self.ble_client:
            return self.ble_client.connect()

    def read_gatt_char(self, uuid):
        if self.ble_client:
            return self.ble_client.read_gatt_char(uuid)

    def write_gatt_char(self, uuid, value, response=False):
        if self.ble_client:
            return self.ble_client.write_gatt_char(uuid, value, response)
        
ble_client = BleClientManager()
@app.get("/enable_Wifi")
async def enableWifi():
    try:
        ssid, password, client = await enable_wifi()
        ble_client.set_client(client)

        print(ble_client.ble_client.services)

        return {"Nombre de Red": ssid, "Contraseña": password}

    except Exception as e:
        logger.error(e)

@app.get("/courtPhoto")
async def courtPhoto():
    try:
        # Synchronization event to wait until notification response is received
        async def runCommands():

            event = asyncio.Event()

            # UUIDs to write to and receive responses from
            COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
            COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
            response_uuid = COMMAND_RSP_UUID

            print(ble_client.ble_client.services)


            def notification_handler(handle: int, data: bytes) -> None:
                logger.info(f'Received response at {handle}: {data.hex(":")}')

                # If this is the correct handle and the status is success, the command was a success
                if ble_client.ble_client.services.characteristics[handle].uuid == response_uuid and data[2] == 0x00:
                    logger.info("Command sent successfully")
                # Anything else is unexpected. This shouldn't happen
                else:
                    logger.error("Unexpected response")

                # Notify the writer
                event.set()

            for service in ble_client.ble_client.services:
                    print(f"Service UUID: {service.uuid}")
                    for char in service.characteristics:
                        print(f"Characteristic UUID: {char.uuid}")

                        if "notify" in char.properties:
                            logger.info(
                                f"Enabling notification on char {char.uuid}")
                            # type: ignore
                            await ble_client.ble_client.start_notify(char, notification_handler)
            logger.info("Done enabling notifications")

            # Write to command request BleUUID to turn the shutter on
            logger.info("Setting photo mode")
            event.clear()
            await ble_client.ble_client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x04, 0x3E, 0x02, 0x03, 0xE9]), response=True)
            await event.wait()  # Wait to receive the notification response

            time.sleep(2)  # If we're recording, let's wait 2 seconds (i.e. take a 2 second video)
            # Write to command request BleUUID to turn the shutter off
            logger.info("Setting the shutter on")
            # event.clear()
            await ble_client.ble_client.write_gatt_char(COMMAND_REQ_UUID, bytearray([3, 1, 1, 1]), response=True)
            await event.wait()  # Wait to receive the notification response

            return

        await runCommands()

        time.sleep(2)
        
        url = GOPRO_BASE_URL + "/gopro/media/list"
        logger.info(f"Getting GoPro's status and settings: sending {url}")

        # Send the GET request and retrieve the response
        response = requests.get(url, timeout=10)
        media_list = response.json()

        print(media_list)

    # Find the last photo with .jpg extension
        photo: Optional[str] = None
        photos = [x["n"] for x in media_list["media"][0]["fs"] if x["n"].lower().endswith(".jpg")]

        if photos:
            photo = photos[-1]  # Select the last photo with .jpg extension
        else:
            raise RuntimeError("Couldn't find a photo on the GoPro")

        # Resto del código es igual

        assert photo is not None
        # Build the URL to get the thumbnail data for the photo
        logger.info(f"Downloading {photo}")
        url = GOPRO_BASE_URL + f"/videos/DCIM/100GOPRO/{photo}"
        logger.info(f"Sending: {url}")
        with requests.get(url, stream=True, timeout=10) as request:
            request.raise_for_status()
            file = photo.split(".")[0] + ".jpg"
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
        logger.info(f"Tamaño del archivo local: {os.path.getsize(file)} bytes")

        blob_client = container_client.get_blob_client(blob_name)

        with open(file, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
        logger.info(f"Archivo '{blob_name}' cargado correctamente en Azure.")


        # Obtener la URL del blob
        blob_url = blob_client.url

        return {"message": "Camera connected", "file_url": blob_url}

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)


@app.get("/record")
async def record():
    try:
        async def runCommands():

            event = asyncio.Event()

            # UUIDs to write to and receive responses from
            COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
            COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
            response_uuid = COMMAND_RSP_UUID

            print(ble_client.ble_client.services)

            print("holaaaa")



            def notification_handler(handle: int, data: bytes) -> None:
                logger.info(f'Received response at {handle}: {data.hex(":")}')

                # If this is the correct handle and the status is success, the command was a success
                if ble_client.ble_client.services.characteristics[handle].uuid == response_uuid and data[2] == 0x00:
                    logger.info("Command sent successfully")
                # Anything else is unexpected. This shouldn't happen
                else:
                    logger.error("Unexpected response")

                # Notify the writer
                event.set()

            for service in ble_client.ble_client.services:
                    print(f"Service UUID: {service.uuid}")
                    for char in service.characteristics:
                        print(f"Characteristic UUID: {char.uuid}")
                        if "notify" in char.properties:
                            logger.info(
                                f"Enabling notification on char {char.uuid}")
                            # type: ignore
                            await ble_client.ble_client.start_notify(char, notification_handler)
            logger.info("Done enabling notifications")

            

            logger.info("Setting video mode")
            event.clear()
            await ble_client.ble_client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x04, 0x3E, 0x02, 0x03, 0xE8]), response=True)
            await event.wait() 

            return

        await runCommands()
        url = GOPRO_BASE_URL + "/gopro/camera/setting?setting=167&option=2"
        logger.info(f"Getting GoPro's status and settings: sending {url}")

        # Send the GET request and retrieve the response
        response = requests.get(url, timeout=10)
        data = response.json()

        return {"message": "Record started"}

    except Exception as e:
        logger.error(e)


@app.get("/stopRecording")
async def stopRecording():
    try:
        async def runCommands():

            event = asyncio.Event()

            # UUIDs to write to and receive responses from
            COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
            COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
            response_uuid = COMMAND_RSP_UUID

            print("holaaaa")
            

            def notification_handler(handle: int, data: bytes) -> None:
                logger.info(f'Received response at {handle}: {data.hex(":")}')

                # If this is the correct handle and the status is success, the command was a success
                if ble_client.ble_client.services.characteristics[handle].uuid == response_uuid and data[2] == 0x00:
                    logger.info("Command sent successfully")
                # Anything else is unexpected. This shouldn't happen
                else:
                    logger.error("Unexpected response")

                # Notify the writer
                event.set()

            for service in ble_client.ble_client.services:
                    for char in service.characteristics:
                        if "notify" in char.properties:
                            logger.info(
                                f"Enabling notification on char {char.uuid}")
                            # type: ignore
                            await ble_client.ble_client.start_notify(char, notification_handler)
            logger.info("Done enabling notifications")


            logger.info("Setting the shutter on")
            event.clear()
            await ble_client.ble_client.write_gatt_char(COMMAND_REQ_UUID, bytearray([3, 1, 1, 1]), response=True)
            await event.wait() 

            time.sleep(2)  
            logger.info("Setting the shutter off")
            # event.clear()
            await ble_client.ble_client.write_gatt_char(COMMAND_REQ_UUID, bytearray([3, 1, 1, 0]), response=True)
            await event.wait() 


            url = GOPRO_BASE_URL + "/gopro/camera/setting?setting=167&option=4"
            logger.info(f"Getting GoPro's status and settings: sending {url}")

            # Send the GET request and retrieve the response
            response = requests.get(url, timeout=10)
            data = response.json()

            return

        await runCommands()

        url = GOPRO_BASE_URL + "/gopro/media/list"
        logger.info(f"Getting GoPro's status and settings: sending {url}")

        # Send the GET request and retrieve the response
        response = requests.get(url, timeout=10)
        media_list = response.json()

    # Find the last photo with .jpg extension
        video: Optional[str] = None
        videos = [x["n"] for x in media_list["media"][0]["fs"] if x["n"].lower().endswith(".mp4")]

        if videos:
            video = videos[-1]  # Select the last photo with .jpg extension
        else:
            raise RuntimeError("Couldn't find a photo on the GoPro")

        # Resto del código es igual

        assert video is not None
        # Build the URL to get the thumbnail data for the video
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
        logger.info(f"Tamaño del archivo local: {os.path.getsize(file)} bytes")

        blob_client = container_client.get_blob_client(blob_name)

        with open(file, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)
        logger.info(f"Archivo '{blob_name}' cargado correctamente en Azure.")


        # Obtener la URL del blob
        blob_url = blob_client.url

        return {"message": "Camera connected", "file_url": blob_url}

    except Exception as e:
        logger.error(e)


@app.get("/getBattery")
async def getBattery():
    try:
        url = GOPRO_BASE_URL + "/gopro/camera/state"
        logger.info(f"Getting GoPro's status and settings: sending {url}")

        # Send the GET request and retrieve the response
        response = requests.get(url, timeout=10)
        data = response.json()

        return {"message": "Battery here :)", "battery": data["status"]["70"]}

    except Exception as e:
        logger.error(e)

  
