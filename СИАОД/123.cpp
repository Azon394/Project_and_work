#include <iostream>
#include <math.h>
using namespace std;

double Halfy(double a, double b, double e, double (*f)(double))
{
    double fa;
    if (a > b) swap(a,b);
    if ((fa = f(a)) * f(b) > 0) throw runtime_error("Wrong data");

    while (b - a > 2 * e) {
        double c = (a + b) / 2;
        if (fa * f(c) < 0)
        {
            b = c;
        }
        else
        {
            a = c;
        }
    }
    return (a + b) / 2;
}

double f(double x) {
    return exp(x) + exp(-3*x) - 4;
}



int main() {
    cout << Halfy(0, 10, 0.0001, f) << endl;
}