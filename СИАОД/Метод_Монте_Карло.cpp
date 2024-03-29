#include <iostream>
#include <cmath>
#include <vector>
#include <tuple>

using namespace std;



double f(double x) {
    return (1/(abs(x) + 0.01));
    //(log(sin(x)) - pow(x, -2)) - гладкая
    //(1/(abs(x) + 0.01)) - острая
    //sin(x) - переодическая
}

tuple<double, double> findMaxandMin(double a, double b) { // функция для определения верхней и нижней границы прямоугольника
    double maxy = -1000000000;
    double miny = 10000000000;
    double dx = (b-a)/10000; // шаг
    for (int i = 0; i <= 10001; i++) {
        double y = f(a+(dx*i));
        if (y > maxy) {
            maxy = y;
        } 
        if (y < miny) {
            miny = y;
        }
    }
    return {maxy, miny};
}

double dRand(double Minx, double Maxx) // функция для получения случайного чилса в определённом диапазоне
{
    double d = (double)rand() / RAND_MAX;
    return Minx + d * (Maxx - Minx);
}

int main() {
    srand (time(NULL)); // чтобы функция rand работала каждый раз по разному
    double a, b, maxy, miny, S, integ, y, x, n;
    double count = 0; // счётчик попаданий
    cout << "a, b, number_of_shoots = " << endl;
    cin >> a >> b >> n; // считываем левую и правую границы и число случайныз бросков
    tie(maxy, miny) = findMaxandMin(a, b); // определяем верхнюю и нижнюю границы
    S = (b - a) * (maxy - miny); // площадь выделенного прямоугольника, в котором находиться наша функция
	for (int i = 0; i < n; i++) { 
        // получаем кординаты случайной точки
        x = dRand(a, b);
        y = dRand(miny, maxy);
        if (y <= f(x) && y >= 0) { // проверяем лежит ли точка в области под функцией
            count++;
        }
        else if (y >= f(x) && y <= 0) { // проверяем лежит ли точка в области над функцией
            count--;
        }
    }
    cout << endl;
    integ = S*count/n; // считыаем отношение точек попавших в область функции ко всем точкам и умнажаем на площадь прямоугольника чтобы получить приближённое значение интеграла
    cout << integ;
}