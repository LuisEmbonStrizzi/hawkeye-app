import asyncio
import time
import requests
from tutorial.tutorial_modules.tutorial_5_connect_wifi.wifi_enable import enable_wifi
from tutorial.tutorial_modules.tutorial_2_send_ble_commands.ble_command_set_shutter import main as ble_command_set_shutter
from tutorial.tutorial_modules.tutorial_6_send_wifi_commands.send_wifi_command import main as send_wifi_command
from tutorial_modules import GOPRO_BASE_URL, logger
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_media_list import get_media_list
from tutorial_modules.tutorial_6_send_wifi_commands.wifi_command_get_state import main as get_camera_state
# Reemplaza 'URL_DEL_BACKEND' con la URL real del backend que deseas consultar.
url_connect_comeras = 'URL_DEL_BACKEND'
# Cambia este valor al intervalo de tiempo deseado en segundos.
intervalo_tiempo_segundos = 60


async def connect_to_cameras():
    await enable_wifi()


# Define las URLs de los 4 backends que deseas consultar junto con sus respuestas correspondientes y las funciones asociadas.
urls_respuestas = {
    'URL_BACKEND_1': {
        'respuesta_esperada': 'ConnectCameras',
        'funcion_a_ejecutar': lambda: asyncio.run(connect_to_cameras())
    },
    'URL_BACKEND_2': {
        'respuesta_esperada': 'StartRecord',
        'funcion_a_ejecutar': lambda: asyncio.run(record())
    },
    'URL_BACKEND_3': {
        'respuesta_esperada': 'Respuesta 3',
        'funcion_a_ejecutar': lambda: asyncio.run(stopRecording())
    },
    'URL_BACKEND_4': {
        'respuesta_esperada': 'Respuesta 4',
        'funcion_a_ejecutar': lambda: asyncio.run(mi_funcion_asincrona())
    }
}

# Cambia este valor al intervalo de tiempo deseado en segundos.
intervalo_tiempo_segundos = 60


async def connect_to_cameras():
    await enable_wifi()
    print("Cameras connected")


async def record():
    send_wifi_command("/gopro/camera/setting?setting=167&option=2")
    await ble_command_set_shutter([3, 1, 1, 1])
    print("Record started")


async def stopRecording():
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

    return file


async def getBattery():
    response = get_camera_state()
    data = response.json()
    return {"message": "Battery here :)", "battery": data["status"]["70"]}

while True:
    for url, info in urls_respuestas.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                respuesta_esperada = info['respuesta_esperada']
                if response.text == respuesta_esperada:
                    print(
                        f"La respuesta de {url} coincide con la esperada: {respuesta_esperada}")
                    funcion_a_ejecutar = info['funcion_a_ejecutar']
                    funcion_a_ejecutar()  # Ejecuta la función asíncrona
                else:
                    print(
                        f"La respuesta de {url} no coincide con la esperada.")
            else:
                print(f"Error en la solicitud a {url}: {response.status_code}")

        except Exception as e:
            print(f"Error en la solicitud a {url}: {str(e)}")

    # Espera el intervalo de tiempo antes de hacer la siguiente ronda de solicitudes
    time.sleep(intervalo_tiempo_segundos)

# El bucle continuará ejecutándose hasta que lo detengas manualmente.

# El bucle continuará ejecutándose hasta que lo detengas manualmente.
