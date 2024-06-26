#include <iostream>
#include <vector>
#include <cmath>
using namespace std;

/*double f1(double x, double y) {
    return sin(y - 0.5) - x -1;
}
double f2(double x, double y) {
    return cos(x-2) + y;
}*/

// Функции системы и их производные
double f1(double x, double y) {
    return sin(y - 0.5) - x -1;
}
double f2(double x, double y) {
    return cos(x-2) + y;
}
double df1dx(double x, double y) {
    return -1;
}
double df1dy(double x, double y) {
    return cos((2*y-1)/2);
}
double df2dx(double x, double y) {
    return -sin(x-2);
}
double df2dy(double x, double y) {
    return 1;
}

// Вектор-функция F(x, y)
vector<double> F(double x, double y) {
    return {f1(x, y), f2(x, y)};
}

// Матрица Якоби
vector<vector<double>> Jacobian(double x, double y) {
    return {{df1dx(x, y), df1dy(x, y)},
            {df2dx(x, y), df2dy(x, y)}};
}

// Метод Ньютона-Рафсона
vector<double> newtonRaphson(double x0, double y0, double eps) {
    double x = x0, y = y0;
    vector<double> Fx = F(x, y);
    int i = 0;
    while (abs(Fx[0]) > eps || abs(Fx[1]) > eps) {
        vector<vector<double>> J = Jacobian(x, y);
        double detJ = J[0][0]*J[1][1] - J[0][1]*J[1][0];
        if (abs(detJ) < eps) {
            throw runtime_error("Матрица Якоби вырождена, решения не существует.");
        }
        double dx = (J[1][1]*Fx[0] - J[0][1]*Fx[1]) / detJ;
        double dy = (J[0][0]*Fx[1] - J[1][0]*Fx[0]) / detJ;
        x -= dx;
        y -= dy;
        Fx = F(x, y);
        i++;
    }
    cout << i << endl;
    return {x, y};
}

int main() {
    double x0, y0, eps;
    cout << "Введите начальное приближение x0, y0: ";
    cin >> x0 >> y0;
    cout << "Введите точность eps: ";
    cin >> eps;
    /*try {
        vector<double> roots = newtonRaphson(x0, y0, eps);
        cout << "Найденные корни системы уравнений: x = " << roots[0] << ", y = " << roots[1] << endl;
    } catch (const exception& e) {
        cerr << "Ошибка: " << e.what() << endl;
    }*/
    vector<double> roots = newtonRaphson(x0, y0, eps);
    cout << "Найденные корни системы уравнений: x = " << roots[0] << ", y = " << roots[1] << endl;
    cout << f1(roots[0], roots[1]) << endl;
    cout << f2(roots[0], roots[1]) << endl;
}
//x = 0.664594, y = 0.581926