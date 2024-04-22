#include <vector>
#include <cmath>
#include <limits>
#include <iostream>

std::vector<std::vector<double>> get_coefficients(int _pl, std::vector<double> _xi) {
    int n = _xi.size();
    std::vector<std::vector<double>> coefficients(n, std::vector<double>(2, 0));
    for (int i = 0; i < n; i++) {
        if (i == _pl) {
            coefficients[i][0] = std::numeric_limits<double>::infinity();
            coefficients[i][1] = std::numeric_limits<double>::infinity();
        } else {
            coefficients[i][0] = 1 / (_xi[_pl] - _xi[i]);
            coefficients[i][1] = -_xi[i] / (_xi[_pl] - _xi[i]);
        }
    }
    std::vector<std::vector<double>> filtered_coefficients(n - 1, std::vector<double>(2, 0));
    int j = 0;
    for (int i = 0; i < n; i++) {
        if (coefficients[i][0] != std::numeric_limits<double>::infinity()) {
            filtered_coefficients[j][0] = coefficients[i][1];
            filtered_coefficients[j][1] = coefficients[i][0];
            j++;
        }
    }
    return filtered_coefficients;
}

std::vector<std::vector<double>> get_polynomial_l(std::vector<double> _xi) {
    int n = _xi.size();
    std::vector<std::vector<double>> pli(n, std::vector<double>(n, 0));
    for (int pl = 0; pl < n; pl++) {
        std::vector<std::vector<double>> coefficients = get_coefficients(pl, _xi);
        for (int i = 1; i < n - 1; i++) {
            if (i == 1) {
                pli[pl][0] = coefficients[i - 1][0] * coefficients[i][0];
                pli[pl][1] = coefficients[i - 1][1] * coefficients[i][0] + coefficients[i][1] * coefficients[i - 1][0];
                pli[pl][2] = coefficients[i - 1][1] * coefficients[i][1];
            } else {
                std::vector<double> clone_pli(n, 0);
                for (int val = 0; val < n; val++) {
                    clone_pli[val] = pli[pl][val];
                }
                std::vector<double> zeros_pli(n, 0);
                for (int j = 0; j < n - 1; j++) {
                    double product_1 = clone_pli[j] * coefficients[i][0];
                    double product_2 = clone_pli[j] * coefficients[i][1];
                    zeros_pli[j] += product_1;
                    zeros_pli[j + 1] += product_2;
                }
                for (int val = 0; val < n; val++) {
                    pli[pl][val] = zeros_pli[val];
                }
            }
        }
    }
    return pli;
}

std::vector<double> get_polynomial(std::vector<double> _xi, std::vector<double> _yi) {
    int n = _xi.size();
    std::vector<std::vector<double>> polynomial_l = get_polynomial_l(_xi);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            polynomial_l[i][j] *= _yi[i];
        }
    }
    std::vector<double> L(n, 0);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            L[i] += polynomial_l[j][i];
        }
    }
    return L;
}

double f(double x) {
    return 1.75+1.81*x-0.6675*x*x+0.115*pow(x,3)-0.0075*pow(x,4);
}

int main() {
    std::vector<double> xi = {1, 2, 3, 4, 5};
    std::vector<double> yi = {3, 3.5, 3.67, 3.75, 3.8};
    std::vector<double> L = get_polynomial(xi, yi);
    for (int i = 0; i < 5; i++) {
        std::cout << L[i] << "*x^" << i << ' ';
    }
    std::cout<<f(4.5);

}

