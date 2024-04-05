#include <iostream>
#include <math.h>
using namespace std;

double f(double x) {
    return exp(x) + exp(-3*x) - 4;
}

double f1(double x) {
    return exp(x) -3*exp(-3*x);
}

double Halfy(double a, double b, double e, double (*f)(double)) {
    //if (f(a) * f(b) > 0) throw runtime_error("Wrong data");

    while (b - a > 2 * e) {
        double c = (a + b) / 2;
        if (f(a) * f(c) < 0) {
            b = c;
        }
        else {
            a = c;
        }
    }
    return (a + b) / 2;
}

double Neuton(double x0, double eps) {
    double h = f(x0) / f1(x0); //Корректирующие приращение поправки
    int c = 0;
    while(abs(h) > eps) {
        h = f(x0) / f1(x0);
        x0 = x0 - h;
        c++;
        //cout << "x" << c << "=" << x0 << endl;
    }
    return x0;
}

int main() {
    double a, b, eps, h;
    cout << "a, b, eps = " << endl;
    cin >> a >> b >> eps;
    if (a > b) swap(a,b);
    h = (b-a)/100;
    cout ;
    for (double i = a; i <= b; i += h ) {
        if (f(i) * f(i+h) <= 0) {
            cout << "Dih: " << Halfy(i, i+h, eps, f) << endl;
            cout << endl << "Nut: " << Neuton((i+(h/2)), eps) << endl;
        }
    }

}