FROM ubuntu:latest

WORKDIR /prueba

RUN apt-get update
RUN apt-get install -y python3 g++ python3-pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install opencv-python

COPY ./Python/speedtest.py .
COPY ./C++/cpplibrary.cpp .

RUN g++ -fPIC -shared -o cpplibrary.so cpplibrary.cpp

CMD [ "python3" , "speedtest.py" ]