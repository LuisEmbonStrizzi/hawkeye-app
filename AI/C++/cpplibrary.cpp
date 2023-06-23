#include <iostream>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc/imgproc.hpp>
#include <vector>

//using namespace cv;

extern "C" {
    std::vector<std::vector<cv::Point>>* abrir_img(void* image_ptr, int alto_OG, int ancho_OG, int channels) {
        unsigned char* image_data = static_cast<unsigned char*>(image_ptr);

        int resizer = 3;

        cv::Mat frame(alto_OG, ancho_OG, CV_8UC3, image_data);

        cv::resize(frame, frame, cv::Size(ancho_OG * resizer, alto_OG * resizer), 0, 0, cv::INTER_AREA);

        cv::GaussianBlur(frame, frame, cv::Size(11, 11), 0);
        cv::cvtColor(frame, frame, cv::COLOR_BGR2HSV);

        cv::Mat mask;
        cv::inRange(frame, cv::Scalar(29, 50, 110), cv::Scalar(64, 255, 255), mask); //greenLower = [29, 50, 110] greenUpper = [64, 255, 255]
        
        // Dos iteraciones de la erosión
        cv::erode(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));
        cv::erode(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));

        // Dos iteraciones de la dilatación
        cv::dilate(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));
        cv::dilate(mask, mask, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3)));

        std::vector<std::vector<cv::Point>> contornos;

        cv::findContours(mask, contornos, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        std::vector<std::vector<cv::Point>> *cnts = new std::vector<std::vector<cv::Point>>(contornos);

        return cnts;
    }
}