#include <iostream>
using namespace std;

double* gauss(double** a, double* y, int n, double eps) {
    double* x, max;
    int k, index;
    x = new double[n];
    k = 0;
    while (k < n) {
        // Поиск строки с максимальным a[i][k]
        max = abs(a[k][k]);
        index = k;
        for (int i = k + 1; i < n; i++) {
            if (abs(a[i][k]) > max) {
                max = abs(a[i][k]);
                index = i;
            }
        }
        // Перестановка строк
        if (max < eps) {
            // нет ненулевых диагональных элементов
            cout << "Решение получить невозможно из-за нулевого столбца ";
            cout << index << " матрицы A" << endl;
            return 0;
        }
        for (int j = 0; j < n; j++) {
            double temp = a[k][j];
            a[k][j] = a[index][j];
            a[index][j] = temp;
        }
        double temp = y[k];
        y[k] = y[index];
        y[index] = temp;
        // Нормализация уравнений
        for (int i = k; i < n; i++) {
            double temp = a[i][k];
            if (abs(temp) < eps) continue; // для нулевого коэффициента пропустить
            for (int j = k; j < n; j++)
                a[i][j] = a[i][j] / temp;
            y[i] = y[i] / temp;
            if (i == k)  continue; // уравнение не вычитать само из себя
            for (int j = 0; j < n; j++)
                a[i][j] = a[i][j] - a[k][j];
            y[i] = y[i] - y[k];
        }
        k++;
    }
    // обратная подстановка
    for (k = n - 1; k >= 0; k--) {
        x[k] = y[k];
        for (int i = 0; i < k; i++)
            y[i] = y[i] - a[i][k] * x[k];
    }
    return x;
}
int main() {
    double** a, * y, * x; // создаём переменные
    double eps;
    int n;
    cout << "Введите количество уравнений: ";
    cin >> n; // считываем кол-во уравнений
    a = new double* [n]; // создаём квадратную матрицу для коэффициентов
    y = new double[n]; // создаём матрицу для правой части уравнения
    for (int i = 0; i < n; i++) {
        a[i] = new double[n]; // досоздаём матрицу для коэффициентов
        for (int j = 0; j < n; j++) {
            cout << "a[" << i << "][" << j << "] = ";
            cin >> a[i][j]; // считываем коэффициенты
        }
    }
    for (int i = 0; i < n; i++) {
        cout << "y[" << i << "]= ";
        cin >> y[i]; // считываем правую часть уравнения
    }
    //2 -1 0 0 5 2 1 -1 3
    //3 7 4
    cout << "eps = ";
    cin >> eps; // считываем погрешность
    x = gauss(a, y, n, eps); // вычисляем решение СЛАУ с помощью метода Гауса
    for (int i = 0; i < n; i++)
        cout << "x[" << i << "]=" << x[i] << endl; // вывод решения СЛАУ
}

//