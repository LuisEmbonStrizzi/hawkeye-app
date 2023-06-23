FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update && apt-get install -y \
    #Para que no me muestre el timezone 
    tcl \
    g++ \
    python3-dev \
    cmake \
    libopencv-dev 

RUN apt-get install -y python3-pip
WORKDIR /app

COPY ./Python/requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY ./C++/cpplibrary.cpp /app/
COPY ./Python/speedtest.py /app/
COPY ./Python/app.py /app/
COPY ./InkedInkedTennisBrothersVideo1080p.mp4 /app/


# -o main especifica el nombre del archivo de salida como main.
# main.cpp es el archivo fuente que deseas compilar.
# -I/usr/include/opencv4 agrega la ruta de inclusión /usr/include/opencv4 para que el compilador pueda encontrar los archivos de encabezado de OpenCV.
# -lopencv_core, -lopencv_highgui, -lopencv_imgcodecs -lopencv_imgproc enlazan las bibliotecas opencv_core, opencv_highgui y libopencv_imgcodecs, libopencv_imgproc.so respectivamente.

RUN g++ -fPIC -shared -o cpplibrary.so cpplibrary.cpp -I/usr/include/opencv4 -lopencv_core -lopencv_highgui -lopencv_imgcodecs -lopencv_imgproc

EXPOSE 8080
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8080"]

# COMANDOS UTILIZADOS DENTRO DEL CONTAINER CON LA IMAGEN DE UBUNTU:
# find /usr/include/ -name highgui.hpp --> para buscar el archivo highgui.hpp y tener la ruta de este
# dpkg -l libopencv-dev --> para ver si esta instalado opencv y ver en que ruta está instalado