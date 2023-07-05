FROM python:3.9

WORKDIR /app

COPY ./gopro.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "gopro:app", "--host=0.0.0.0", "--port=80"]