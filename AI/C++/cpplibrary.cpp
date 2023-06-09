#include <iostream>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc/imgproc.hpp>

extern "C"
{
    unsigned char *procesar_frame(unsigned char *image_ptr, int alto_OG, int ancho_OG, int channels)
    {
        unsigned char *image_data = static_cast<unsigned char *>(image_ptr);

        int resizer = 3;

        cv::Mat frame(alto_OG, ancho_OG, CV_8UC3, image_data);

        cv::resize(frame, frame, cv::Size(ancho_OG * resizer, alto_OG * resizer), 0, 0, cv::INTER_AREA);

        cv::GaussianBlur(frame, frame, cv::Size(11, 11), 0);
        cv::cvtColor(frame, frame, cv::COLOR_BGR2HSV);

        cv::Mat mask;
        cv::inRange(frame, cv::Scalar(29, 50, 110), cv::Scalar(64, 255, 255), mask); // greenLower = [29, 50, 110] greenUpper = [64, 255, 255]

        // Dos iteraciones de la erosión
        cv::erode(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));
        cv::erode(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));

        // Dos iteraciones de la dilatación
        cv::dilate(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));
        cv::dilate(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));

        // Crear un nuevo bloque de memoria para los datos de la imagen modificada
        unsigned char *imagen_modificada_data = (unsigned char *)malloc(alto_OG * resizer * ancho_OG * resizer);

        // Copiar los datos de la imagen modificada al nuevo bloque de memoria
        std::memcpy(imagen_modificada_data, mask.data, alto_OG * resizer * ancho_OG * resizer);

        return imagen_modificada_data;
    }
}