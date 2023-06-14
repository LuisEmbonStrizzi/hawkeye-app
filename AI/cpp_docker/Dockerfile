FROM ubuntu:latest


RUN apt-get update && apt-get install -y \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN g++ -fPIC -shared -o main.so main.cpp

CMD ["python3", "test.py"]

