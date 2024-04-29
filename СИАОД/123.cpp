#include <iostream>
#include <cmath>

using namespace std;
typedef double(*pointFunc)(double, double);

double f(double x, double k) {
    return x;
}

double fc(double x, double k) {
    return f(x,k)*cos(k*x);
}

double fs(double x, double k) {
    return f(x,k)*sin(k*x);
}

// функция для нахождения середины между a и b, значении функции в этой середине, нахождения грубого интегрирования по методу симпсона через эти 3 точки
std::tuple<double, double, double> quad_simpsons_mem(pointFunc f, double a, double fa, double b, double fb, int k) {
    double m = (a + b) / 2; // середина
    double fm = f(m, k); // значение функции в середине
    double result = std::abs(b - a) / 6 * (fa + 4 * fm + fb); // грубое значение интеграла
    return std::make_tuple(m, fm, result);
}
double quad_asr(pointFunc f, double a, double fa, double b, double fb, double eps, double whole, double m, double fm, int k) {
    double lm, flm, left;
    std::tie(lm, flm, left) = quad_simpsons_mem(f, a, fa, m, fm, k); // вычисление интеграла слева
    double rm, frm, right;
    std::tie(rm, frm, right) = quad_simpsons_mem(f, m, fm, b, fb, k); // вычисление интеграла справа
    double delta = left + right - whole; // считаем разницу между значением интеграла до разделения и после
    // если разница меньше чем допустимая погрешность то возвращаем результат
    if (std::abs(delta) <= 15 * eps) {
        return left + right + delta / 15;
    }
    // если нужная разница не достигнута то делим ось X пополам и считаем отдельно интеграл левой и правой части, а потом их значения складываем
    return quad_asr(f, a, fa, m, fm, eps / 2, left, lm, flm, k) +
           quad_asr(f, m, fm, b, fb, eps / 2, right, rm, frm, k);
}

double integ(pointFunc f, double a, double b, double eps, int k) {
    //cout << "2) " << f(1, k) << endl;
    double fa = f(a, k);
    double fb = f(b, k);
    double m, fm, whole, result;
    std::tie(m, fm, whole) = quad_simpsons_mem(f, a, fa, b, fb, k);
    result = quad_asr(f, a, fa, b, fb, eps, whole, m, fm, k);
    return result;
}

int main() {
    double T;
    int M;
    double *As, *Bs;
    cout << "Введите T, M ";
    cin >> T >> M;
    As = new double[M];
    Bs = new double[M];
    Bs[0] = 0;
    As[0] = (2/T) * integ(f, 0, T, 0.001, 0);
    cout << As[0]/2;
    for (int k = 1; k < M+1; k++) {
        As[k] = (2/T) * integ(fc, 0, T, 0.001, k);
        Bs[k] = (2/T) * integ(fs, 0, T, 0.001, k);
        if (As[k] >= 0) {
            cout << "+";
        }
        cout << As[k] << "*cos(" << k << "x)";
        if (Bs[k] >= 0) {
            cout << "+";
        }
        cout << Bs[k] << "*sin(" << k << "x)";
    }

}

