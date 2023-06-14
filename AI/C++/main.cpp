#include <iostream>
#include <opencv2/opencv.hpp>

using namespace cv;

int main(int, char**) {
    Mat image;
    image = imread("./AI/imagenPrueba.png");

    imshow("testeando...", image);

    return 0;
}
