#include <opencv4/opencv2/highgui.hpp> //Ruta de opencv en el docker
#include <iostream>
extern "C"
{

    int main(int argc, char **argv)
    {

        cv::Mat image;
        image = cv::imread("./descarga.jpg", cv::IMREAD_COLOR);

        if (!image.data)
        {
            std::cout << "Could not open or find the image" << std::endl;
            return -1;
        }

        cv::Mat smoothed_image;
        cv::GaussianBlur(image, smoothed_image, cv::Size(5, 5), 0);

        cv::imwrite("/app/result.jpg", image);

        std::cout << "Image saved successfully" << std::endl;

        return 0;
    }
}