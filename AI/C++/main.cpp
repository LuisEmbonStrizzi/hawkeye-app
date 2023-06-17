#include <iostream>
#include <opencv4/opencv2/highgui.hpp>
#include <opencv4/opencv2/imgproc/imgproc.hpp>

using namespace cv;

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
}
