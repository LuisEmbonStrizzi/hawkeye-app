#include <iostream>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc/imgproc.hpp>

using namespace cv;

extern "C" {
    void abrir_img(void* image_ptr, int alto_OG, int ancho_OG, int channels, int* result_ptr) {
        unsigned char* image_data = static_cast<unsigned char*>(image_ptr);

        int resizer = 3;

        Mat frame(alto_OG, ancho_OG, CV_8UC3, image_data);

        resize(frame, frame, Size(ancho_OG * resizer, alto_OG * resizer), 0, 0, INTER_AREA);

        GaussianBlur(frame, frame, Size(11, 11), 0);
        cvtColor(frame, frame, COLOR_BGR2HSV);

        Mat mask;
        inRange(frame, Scalar(29, 50, 110), Scalar(64, 255, 255), mask); //greenLower = [29, 50, 110] greenUpper = [64, 255, 255]
        
        // Dos iteraciones de la erosión
        erode(mask, mask, getStructuringElement(MORPH_RECT, Size(3, 3)));
        erode(mask, mask, getStructuringElement(MORPH_RECT, Size(3, 3)));

        // Dos iteraciones de la dilatación
        dilate(mask, mask, getStructuringElement(MORPH_RECT, Size(3, 3)));
        dilate(mask, mask, getStructuringElement(MORPH_RECT, Size(3, 3)));

        int result = 777;
        *result_ptr = result;
    }
}