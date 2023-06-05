FROM python:3.9

WORKDIR /app

COPY ./app.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]