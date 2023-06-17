FROM ubuntu:latest


#Para que no me muestre el timezone

ENV DEBIAN_FRONTEND noninteractive 

RUN apt-get update && apt-get install -y \
    #Para que no me muestre el timezone 
    tcl \
    g++ \
    python3-dev \
    cmake \
    libopencv-dev 


WORKDIR /app

COPY . /app/

# -o main especifica el nombre del archivo de salida como main.
# main.cpp es el archivo fuente que deseas compilar.
# -I/usr/include/opencv4 agrega la ruta de inclusión /usr/include/opencv4 para que el compilador pueda encontrar los archivos de encabezado de OpenCV.
# -lopencv_core, -lopencv_highgui, -lopencv_imgcodecs enlazan las bibliotecas opencv_core, opencv_highgui y libopencv_imgcodecs, respectivamente.
RUN g++ -o main main.cpp -I/usr/include/opencv4 -lopencv_core -lopencv_highgui -lopencv_imgcodecs

CMD ["./main"]

# COMANDOS UTILIZADOS DENTRO DEL CONTAINER CON LA IMAGEN DE UBUNTU:
# find /usr/include/ -name highgui.hpp --> para buscar el archivo highgui.hpp y tener la ruta de este
# dpkg -l libopencv-dev --> para ver si esta instalado opencv y ver en que ruta está instalado

