#include <iostream>
#include <vector>
#include <algorithm>
#include <math.h>

using namespace std;

double interpolate(const vector<double>& xp, const vector<double>& fp, double x) {
    auto it = lower_bound(xp.begin(), xp.end(), x);
    if (it == xp.begin()) return fp[0];
    if (it == xp.end()) return fp.back();
    int pos = it - xp.begin();
    double x1 = xp[pos - 1], x2 = xp[pos];
    double y1 = fp[pos - 1], y2 = fp[pos];
    return y1 + (x - x1) * (y2 - y1) / (x2 - x1);
}

int main() {
    vector<double> xp;
    vector<double> fp;
    vector<double> xs;
    int action;
    cout << "choose the func: " << endl << "(1) e^x " << endl << "(2) e^-x " << endl << "(3) sh(x) " << endl \
    << "(4) ch(x) " << endl << "(5) sin(x) " << endl << "(6) cos(x) " << endl << "(7) ln(x) " << endl;
    cin >> action;
    if (action == 1) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(exp(i));
            cout << fp.back() << endl;
            xs = {1.07, 1.11, 1.14, 1.15, 1.19};
        }
    } else if (action == 2) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(exp(-i));
            cout << fp.back() << endl;
            xs = {1.05, 1.09, 1.13, 1.15, 1.17};
        }
    } else if (action == 3) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(sinh(i));
            cout << fp.back() << endl;
            xs = {1.05, 1.09, 1.13, 1.15, 1.17};
        }
    } else if (action == 4) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(cosh(i));
            cout << fp.back() << endl;
            xs = {1.05, 1.09, 1.13, 1.15, 1.17};
        }
    } else if (action == 5) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(sin(i));
            cout << fp.back() << endl;
            xs = {1.05, 1.09, 1.13, 1.15, 1.17};
        }
    } else if (action == 6) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(cos(i));
            cout << fp.back() << endl;
            xs = {1.07, 1.11, 1.14, 1.15, 1.19};
        }
    } else if (action == 7) {
        for (double i = 1; i <= 1.2001; i += 0.04) {
            cout << i << " ";
            xp.push_back(i);
            fp.push_back(log(i));
            cout << fp.back() << endl;
            xs = {1.05, 1.09, 1.13, 1.15, 1.17};
        }
    } else {
        double a;
        int n;
        cout << "enter n ";
        cin >> n;
        for (int i = 0; i<n; i++) {
            cout << "enter x" << i+1 << " ";
            cin >> a;
            xp.push_back(a);
            cout << xp[i] << endl;
        }
        for (int i = 0; i<n; i++) {
            cout << "enter y" << i+1 << " ";
            cin >> a;
            fp.push_back(a);
            cout << fp[i] << endl;
        }
    }
    for (double x : xs) {
        double t = interpolate(xp, fp, x);
        cout << "Interpolated value at " << x << ": " << t << endl;
    }
}
