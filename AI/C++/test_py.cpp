#include <iostream>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc/imgproc.hpp>

using namespace cv;

extern "C" {
    void abrir_img(void* image_ptr, int rows, int cols, int channels, int* result_ptr) {
        unsigned char* image_data = static_cast<unsigned char*>(image_ptr);

        Mat image(rows, cols, CV_8UC3, image_data);

        Point center(cols / 2, rows / 2);
        int radius = 50;
        Scalar line_Color(255, 0, 0);
        int thickness = 2;
        circle(image, center,radius, line_Color, thickness);

        imwrite("luis.jpg", image);

        int result = 777;
        *result_ptr = result;
    }
}

/*
int main(int, char**) {
    Mat image;
    image = imread("./imagenPrueba.png");

    Point center(100, 100);
    int radius = 50;
    Scalar line_Color(0, 0, 0);
    int thickness = 2;
    circle(image, center,radius, line_Color, thickness);

    imwrite("luis.jpg", image);

    return 0;
} */