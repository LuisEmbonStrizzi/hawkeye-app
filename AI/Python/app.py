from fastapi import FastAPI
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient
import os
from decouple import config
from ball_tracking2_cpp import tracking
from zoomear_video import zoomear_video

azure_connection_string = config('AZURE_CONNECTION_STRING')
container_name = config('AZURE_CONTAINER_NAME')

app = FastAPI()


class Msg(BaseModel):
    url: str


@app.post("/predict")
async def predict(inp: Msg):

    pique = tracking(inp.url)
    zoomear_video(inp.url, pique)

    file = "video_zoom.mp4"

    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = os.path.basename(file)
    print(f"Tamaño del archivo local: {os.path.getsize(file)} bytes")

    blob_client = container_client.get_blob_client(blob_name)

    with open(file, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    print(f"Archivo '{blob_name}' cargado correctamente en Azure.")

    blob_url = blob_client.url

    return {"file_url": blob_url}