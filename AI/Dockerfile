FROM python:3.9

WORKDIR /app

COPY ./app.py .
COPY ./ball_tracking2.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


EXPOSE 8080
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]