#include <iostream>
#include <cmath>
using namespace std;
typedef double(*pointFunc)(double);

double f(double x) {
    return (x*x+4*x+4);
    //(log(sin(x)) - pow(x, -2)) - гладкая
    //(1/(abs(x) + 0.01)) - острая
    //sin(x) - переодическая
}

// функция для нахождения середины между a и b, значении функции в этой середине, нахождения грубого интегрирования по методу симпсона через эти 3 точки
std::tuple<double, double, double> quad_simpsons_mem(double a, double fa, double b, double fb) {
    double m = (a + b) / 2; // середина
    double fm = f(m); // значение функции в середине
    double result = std::abs(b - a) / 6 * (fa + 4 * fm + fb); // грубое значение интеграла 
    return std::make_tuple(m, fm, result);
}

// рекурсивная функция для вычисления интеграла по частям
double quad_asr(double a, double fa, double b, double fb, double eps, double whole, double m, double fm) {
    double lm, flm, left;
    std::tie(lm, flm, left) = quad_simpsons_mem(a, fa, m, fm); // вычисление интеграла слева
    double rm, frm, right;
    std::tie(rm, frm, right) = quad_simpsons_mem(m, fm, b, fb); // вычисление интеграла справа
    double delta = left + right - whole; // считаем разницу между значением интеграла до разделения и после
    // если разница меньше чем допустимая погрешность то возвращаем результат
    if (std::abs(delta) <= 15 * eps) {
        return left + right + delta / 15;
    }
    // если нужная разница не достигнута то делим ось X пополам и считаем отдельно интеграл левой и правой части, а потом их значения складываем
    return quad_asr(a, fa, m, fm, eps / 2, left, lm, flm) +
           quad_asr(m, fm, b, fb, eps / 2, right, rm, frm);
}

double integ(pointFunc f, double a, double b, double eps) {
    double fa = f(a);
    double fb = f(b);
    double m, fm, whole, result;
    std::tie(m, fm, whole) = quad_simpsons_mem(a, fa, b, fb);
    result = quad_asr(a, fa, b, fb, eps, whole, m, fm);
    return result;
}

int main() {
    /*double a, b, eps, result;
    std::cout << "a, b, eps: " << std::endl;
    std::cin >> a >> b >> eps; // считываем значения
    double fa = f(a);
    double fb = f(b);
    double m, fm, whole;
    std::tie(m, fm, whole) = quad_simpsons_mem(a, fa, b, fb);
    result = quad_asr(a, fa, b, fb, eps, whole, m, fm);;
    std::cout << "Result: " << result << std::endl*/;
    cout << integ(f, 0, 2, 0.001);
}
