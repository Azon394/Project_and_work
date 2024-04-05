#include <iostream>
#include <math.h>
#include <cmath>

using namespace std;

typedef double(*pointFunc)(double);

double f(double x) {
    return (log(sin(x)) - pow(x, -2));     
    //(log(sin(x)) - pow(x, -2)) - гладкая
    //(1/(abs(x) + 0.01)) - острая
    //sin(x) - переодическая
}

double simpson_integral(pointFunc f, double a, double b, int n) {
  double h = (b-a)/n; // шаг
  double k1 = 0, k2 = 0; // переменные для сохранения значений функции в чётных и нечётных точках
  for (int i = 1; i < n-1; i += 2) { // высчитываем значения функции при чётных и нечётных точках исключая крайние точки
    k1 += f(a + i*h);
    k2 += f(a + (i+1)*h);
  }
  return h/3*(f(a) + 4*k1 + 2*k2 + f(b)); // считаем интеграл по формуле
}

int main() {
    double a, b, eps, runge;
    double s1, s;
    int n = 2; //начальное число шагов
    cout << "a, b, eps: " << endl;
    cin >> a >> b >> eps; // считываем значения
    s1 = simpson_integral(f, a, b, n); // первое приближение для интеграла
    do {
        s = s1; // второе приближение
        n = 2 * n; // увеличение числа шагов в два раза,
        s1 = simpson_integral(f, a, b, n); // считаем интеграл для нового кол-ва шагов
        runge = (s1 - s)/15;
    }
    while (abs(runge) > eps);  // сравниваем приближённые значения с заданной точностью
    cout << "\nИнтеграл = " << s1 << endl;
}