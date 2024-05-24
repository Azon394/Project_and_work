#include <iostream>
#include <cmath>
#include <vector>

using namespace std;

double func(vector<double>& coords){
    double x, y;
    x = coords[0];
    y = coords[1];
    return pow((x+5), 2) + pow(y,2);
    // pow((x+5), 2) + pow(y,2);
}

void f1(vector<double>& vars, double h){
    vector<double> vec = vars;
    for(int i = 0; i < vec.size(); i++){
        while(true){
            double p = func(vec);
            vec[i] += h;
            if(p <= func(vec)){
                vec[i] -= 2*h;
                if(p <= func(vec)){
                    vec[i]+=h;
                    break;
                }
            }
        }
    }
    vars = vec;
}

void f2(vector<double>& znach, double h, double eps){
    while(h>eps){
        h/=2;
        f1(znach,h);
    }
}

int main(){
    double x0, y0; // Приближенное начальное значение x для y
    cout << "Начальное приближение x0, y0:";
    cin >> x0 >> y0;
    vector<double> vars {x0, y0}; // Вектор начальных значений
    double h = 0.1; // Наш шаг
    double eps = 0.01; // Минимальное значение шага
    f2(vars,h,eps);
    for(double i : vars){
        cout << i <<" ";
    }
    cout << func(vars);

    return 0;
}