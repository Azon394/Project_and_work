#include <iostream>
using namespace std;

double* iter(double** a, double* y, int n, double eps, int h) {
	double* res = new double[n];
	int i, j;
	for (i = 0; i < n; i++) {
		res[i] = y[i] / a[i][i];
	}
	double* Xn = new double[n];
	do {
		for (i = 0; i < n; i++) {
			Xn[i] = y[i] / a[i][i];
			for (j = 0; j < n; j++) {
				if (i == j)
					continue;
				else {
					Xn[i] -= a[i][j] / a[i][i] * res[j];
				}
			}
		}
		bool flag = true;
		for (i = 0; i < n - 1; i++) {
			if (abs(Xn[i] - res[i]) > eps) {
				flag = false;
				break;
			}
		}

		for (i = 0; i < n; i++) {
			res[i] = Xn[i];
		}
		if (flag)
			break;
	} while (1);
	return res;
}

int main() {
    double** a, * y, * x; // создаём переменные
    double eps;
	int n, h;
	cout << "Введите количество уравнений: ";
	cin >> n;
	y = new double[n];
	a = new double* [n];
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
    cout << "eps = ";
    cin >> eps; // считываем погрешность
    cout << "количество итераций";
    cin >> h;
	x = iter(a, y, n, eps, h);
	for (int i = 0; i < n; i++) {
		cout << x[i] << "\t";
	}
	cout << endl;
}
//2 -1 0 0 5 2 1 -1 3
//3 7 4