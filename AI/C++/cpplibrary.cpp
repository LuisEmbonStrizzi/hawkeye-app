#include <iostream>
using namespace std;

extern "C" {
    int suma(int n1, int n2) {
        return n1 + n2;
    }
}