# /api-gopro/python
import logging
from binascii import hexlify
import re
from typing import Optional
from fastapi import FastAPI, HTTPException
import time
import requests
import asyncio
from azure.storage.blob import BlobServiceClient
import os
from decouple import config
from fastapi.middleware.cors import CORSMiddleware
from bleak import BleakClient
from typing import Dict, Any, List, Callable, Optional, Tuple
from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice as BleakDevice
app = FastAPI()


logger: logging.Logger = logging.getLogger("tutorial_logger")
GOPRO_BASE_UUID = "b5f9{}-aa8d-11e3-9046-0002a5d5c51b"
GOPRO_BASE_URL = "http://10.5.5.9:8080"


def exception_handler(loop: asyncio.AbstractEventLoop, context: Dict[str, Any]) -> None:
    """Catch exceptions from non-main thread

    Args:
        loop (asyncio.AbstractEventLoop): loop to catch exceptions in
        context (Dict[str, Any]): exception context
    """
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception {str(loop)}: {msg}")
    logger.critical("This is unexpected and unrecoverable.")


async def connect_ble(
    notification_handler: Callable[[int, bytes], None],
    identifier: Optional[str] = None,
) -> BleakClient:
    """Connect to a GoPro, then pair, and enable notifications

    If identifier is None, the first discovered GoPro will be connected to.

    Retry 10 times

    Args:
        notification_handler (Callable[[int, bytes], None]): callback when notification is received
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Raises:
        Exception: couldn't establish connection after retrying 10 times

    Returns:
        BleakClient: connected client
    """

    asyncio.get_event_loop().set_exception_handler(exception_handler)

    RETRIES = 10
    for retry in range(RETRIES):
        try:
            # Map of discovered devices indexed by name
            devices: Dict[str, BleakDevice] = {}

            # Scan for devices
            logger.info("Scanning for bluetooth devices...")

            # Scan callback to also catch nonconnectable scan responses
            # pylint: disable=cell-var-from-loop
            def _scan_callback(device: BleakDevice, _: Any) -> None:
                # Add to the dict if not unknown
                if device.name and device.name != "Unknown":
                    devices[device.name] = device

            # Scan until we find devices
            matched_devices: List[BleakDevice] = []
            while len(matched_devices) == 0:
                # Now get list of connectable advertisements
                for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
                    if device.name != "Unknown" and device.name is not None:
                        devices[device.name] = device
                # Log every device we discovered
                for d in devices:
                    logger.info(f"\tDiscovered: {d}")
                # Now look for our matching device(s)
                token = re.compile(
                    r"GoPro [A-Z0-9]{4}" if identifier is None else f"GoPro {identifier}")
                matched_devices = [device for name,
                                   device in devices.items() if token.match(name)]
                logger.info(f"Found {len(matched_devices)} matching devices.")

            # Connect to first matching Bluetooth device
            device = matched_devices[0]

            logger.info(f"Establishing BLE connection to {device}...")
            client = BleakClient(device)
            await client.connect(timeout=120)
            logger.info("BLE Connected!")

            # Try to pair (on some OS's this will expectedly fail)
            logger.info("Attempting to pair...")
            try:
                await client.pair()
            except NotImplementedError:
                # This is expected on Mac
                pass
            logger.info("Pairing complete!")

            # Enable notifications on all notifiable characteristics
            logger.info("Enabling notifications...")
            for service in client.services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        logger.info(
                            f"Enabling notification on char {char.uuid}")
                        # type: ignore
                        await client.start_notify(char, notification_handler)
            logger.info("Done enabling notifications")

            return client
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error(f"Connection establishment failed: {exc}")
            logger.warning(f"Retrying #{retry}")

    raise RuntimeError(
        f"Couldn't establish BLE connection after {RETRIES} retries")


async def enable_wifi(identifier: Optional[str] = None) -> Tuple[str, str, BleakClient]:
    """Connect to a GoPro via BLE, find its WiFi AP SSID and password, and enable its WiFI AP

    If identifier is None, the first discovered GoPro will be connected to.

    Args:
        identifier (str, optional): Last 4 digits of GoPro serial number. Defaults to None.

    Returns:
        Tuple[str, str]: ssid, password
    """
    # Synchronization event to wait until notification response is received
    event = asyncio.Event()

    # UUIDs to write to and receive responses from, and read from
    COMMAND_REQ_UUID = GOPRO_BASE_UUID.format("0072")
    COMMAND_RSP_UUID = GOPRO_BASE_UUID.format("0073")
    WIFI_AP_SSID_UUID = GOPRO_BASE_UUID.format("0002")
    WIFI_AP_PASSWORD_UUID = GOPRO_BASE_UUID.format("0003")

    client: BleakClient

    def notification_handler(handle: int, data: bytes) -> None:
        logger.info(f'Received response at {handle=}: {hexlify(data, ":")!r}')

        # If this is the correct handle and the status is success, the command was a success
        if client.services.characteristics[handle].uuid == COMMAND_RSP_UUID and data[2] == 0x00:
            logger.info("Command sent successfully")
        # Anything else is unexpected. This shouldn't happen
        else:
            logger.error("Unexpected response")

        # Notify the writer
        event.set()

    client = await connect_ble(notification_handler, identifier)

    # Read from WiFi AP SSID BleUUID
    logger.info("Reading the WiFi AP SSID")
    ssid = (await client.read_gatt_char(WIFI_AP_SSID_UUID)).decode()
    logger.info(f"SSID is {ssid}")

    # Read from WiFi AP Password BleUUID
    logger.info("Reading the WiFi AP password")
    password = (await client.read_gatt_char(WIFI_AP_PASSWORD_UUID)).decode()
    logger.info(f"Password is {password}")

    # Write to the Command Request BleUUID to enable WiFi
    logger.info("Enabling the WiFi AP")
    event.clear()
    await client.write_gatt_char(COMMAND_REQ_UUID, bytearray([0x03, 0x17, 0x01, 0x01]), response=True)
    await event.wait()  # Wait to receive the notification response
    logger.info("WiFi AP is enabled")

    return ssid, password, client
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/api-gopro/hello")
def enableWifi():
    try:
        return {"Hola": "hola"}

    except Exception as e:
        logger.error(e)


@app.get("/api-gopro/enable_Wifi")
async def enableWifi():
    try:
        ssid, password, client = await enable_wifi()
        ble_client.set_client(client)

        print(ble_client.ble_client.services)

        return {"networkName": ssid, "password": password}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api-gopro/courtPhoto")
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

            # If we're recording, let's wait 2 seconds (i.e. take a 2 second video)
            time.sleep(2)
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
        photos = [x["n"] for x in media_list["media"][0]
                  ["fs"] if x["n"].lower().endswith(".jpg")]

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
        print(file)

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

        return {"message": "PhotoTaken", "file_url": blob_url}

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api-gopro/record")
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

        return {"message": "RecordStarted"}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api-gopro/stopRecording")
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
        videos = [x["n"] for x in media_list["media"][0]
                  ["fs"] if x["n"].lower().endswith(".mp4")]

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
        return {"message": "CameraConnected", "file_url": blob_url}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api-gopro/getBattery")
async def getBattery():
    try:
        url = GOPRO_BASE_URL + "/gopro/camera/state"
        logger.info(f"Getting GoPro's status and settings: sending {url}")

        # Send the GET request and retrieve the response
        response = requests.get(url, timeout=10)
        data = response.json()

        return {"message": "BatteryHere", "battery": data["status"]["70"]}

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
