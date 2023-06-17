from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get('/image')
def get_image():
    image_path = '/app/result.jpg'
    return FileResponse(image_path, media_type='image/jpeg')
