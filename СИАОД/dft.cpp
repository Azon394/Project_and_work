#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

const double PI = 3.14159265358979323846;

// Функция для вычисления значения многочлена в точке x
double polynomial(const vector<double>& coeffs, double x) {
    double result = 0.0;
    for (int i = 0; i < coeffs.size(); ++i) {
        result += coeffs[i] * pow(x, i);
    }
    return result;
}

// Функция для вычисления коэффициентов ряда Фурье
pair<double, double> calculate_fourier_coeffs(const vector<double>& coeffs, int n, double L) {
    int N = 10000; // Количество точек для численного интегрирования
    double dx = 2.0 * L / N;
    double a = 0.0, b = 0.0;
    for (int i = 0; i < N; ++i) {
        double x = -L + i * dx;
        double fx = polynomial(coeffs, x);
        a += fx * cos(n * PI * x / L) * dx;
        b += fx * sin(n * PI * x / L) * dx;
    }
    a /= L;
    b /= L;
    return {a, b};
}

int main() {
    double L; // Период функции
    int degree; // Степень многочлена
    cout << "Введите период функции L: ";
    cin >> L;
    cout << "Введите степень многочлена: ";
    cin >> degree;
    vector<double> coeffs(degree + 1);
    cout << "Введите коэффициенты многочлена: ";
    for (int i = 0; i <= degree; ++i) {
        cin >> coeffs[i];
    }
    int N; // Количество членов в ряде Фурье
    cout << "Введите количество членов в ряде Фурье: ";
    cin >> N;
    vector<pair<double, double>> fourier_coeffs(N);
    for (int n = 0; n < N; ++n) {
        fourier_coeffs[n] = calculate_fourier_coeffs(coeffs, n, L);
    }
    // Выводим ряд Фурье в виде суммы синусов и косинусов
    cout << "Ряд Фурье: f(x) = ";
    for (int n = 0; n < N; ++n) {
        if (n > 0) {
            cout << " + ";
        }
        cout << fourier_coeffs[n].first << " * cos(" << n << " * pi * x / " << L << ") + " << fourier_coeffs[n].second << " * sin(" << n << " * pi * x / " << L << ")";
    }
    cout <<endl;
    return 0;
}
