/*----------------------------------------------------------------------------------------------------------------------
                                    Программа для разложения функции в ряд Фурье.
 Требуемые для ввода величины:
 f(x) - функция для разложения;
 l - полупериод разложения, положительное вещественное число, допусимы математические константы - см. ниже;
 n - количество членов разложения, натуральное число.

 Для введения функции подразумеваются следующие обозначения:
 +, -, *, / - сложение, вычитание, умножение и деление соответственно. Деление на 0 вызывает завершение работы программы;
 ^ - возведение в степень;
 (, ) - скобки. Неправильная расстановка скобок вызывает завершение работы программы;
 pi = 3.14159265358979323846 - число Пи;
 е = 2.7182818284590452354 - число Эйлера;
 sqrt(a) - квадратный корень числа а. Извлечение корня из отрицательного числа вызывает завершение работы программы;
 abs(a) - абсолютное значение (модуль) числа а;
 sin(a), cos(a), tg(a), ctg(a) - соответственно синус, косинус, тангенс, котангенс числа а;
 arcsin(a), arccos(a) - соответственно арксинус и арккосинус числа а. Подача на вход числа, большего 1 по модулю,
 вызывает завершение работы программы;
 arctg(a), arcctg(a) - соответственно арктангенс и арккотангенс числа а;
 lg(a) - логарифм числа а по основанию 10. Взятие логарифма неположительного числа вызывает завершение работы программы;
 ln(a) - натуральный логарифм числа а. Взятие логарифма неположительного числа вызывает завершение работы программы;
 Все прочие символы при вводе игнорируются.

 При проведении вычислений подразумевается, что f(x) непрерывна и интегрируема на [-l; l]. При невыполнении этого условия
 может произойти непредвиденное завершение работы программы.

 Разработчик: Andrien
 Лицензия GNU GPL
----------------------------------------------------------------------------------------------------------------------*/
#include <iostream>
#include <string>
#include <cmath>
#include <stack>
#include <map>
#include <exception>

#define EPSILON 0.000001 //Предел чувствительности для равенства double
#define INTEGRATION_STEPS 10000
#define PRECISION 5 //количество знаков после запятой при округлении
using namespace std;
//Приоритет операций
map<char, int> priority = {{'+', 1},
                           {'-', 1},
                           {'*', 2},
                           {'/', 2},
                           {'^', 3}};

double round(double x) { //Округление до PRECISION цифр после запятой
    int fl = floor(x);
    if (x - fl < EPSILON) {
        return fl;
    }
    if (ceil(x) - x < EPSILON) {
        return ceil(x);
    }
    double step = 0.1 * PRECISION;
    for (int i = 0; i < (1 / step); i++) {
        double curr = fl + step * i;
        if (abs(curr - x) < EPSILON) {
            return curr;
        }
    }
    return x;
}

string sanitize(string input) { //Удаление незначащих 0 после запятой
    while (input.back() == '0') {
        input.pop_back();
    }
    if (input.back() == '.') {
        input.pop_back();
    }
    return input;
}

string input() { //Обработка ввода
    string str;
    getline(cin, str);
    string p_inp;
    for (char ch: str) { //Удаление пробелов и приведение к строчным буквам
        if (ch != ' ') {
            if (isalpha(ch)) {
                p_inp.push_back(tolower(ch));
            } else {
                p_inp.push_back(ch);
            }
        }
    }
    string res;
    stack<string> queue;
    string curr; //Преобразование в обратную польскую запись
    for (int i = 0; i < p_inp.length(); i++) {
        if (isdigit(p_inp[i]) || p_inp[i] == '.') {
            curr.push_back(p_inp[i]);
        } else if (p_inp[i] == 'x' || p_inp[i] == 'e') {
            res.push_back(p_inp[i]);
            res.push_back(' ');
        } else if (p_inp[i] == 'p' && i < (p_inp.length() - 1) && p_inp[i + 1] == 'i') {
            res.append("pi ");
            i += 1;
        } else {
            if (isdigit(curr.back())) {
                res.append(curr);
                res.push_back(' ');
                curr = "";
            }
            if (p_inp[i] == '-') {
                if (i == 0) {
                    curr.push_back(p_inp[i]);
                } else {
                    if (!isdigit(p_inp[i - 1]) && p_inp[i - 1] != 'x' && p_inp[i - 1] != 'i' && p_inp[i - 1] != 'e' &&
                        p_inp[i - 1] != ')') {
                        curr.push_back(p_inp[i]);
                    } else {
                        while (!queue.empty() && priority[queue.top()[0]] >= priority[p_inp[i]]) {
                            res.append(queue.top());
                            res.push_back(' ');
                            queue.pop();
                        }
                        string c;
                        c.push_back(p_inp[i]);
                        queue.push(c);
                    }
                }
            } else {
                if (isalpha(p_inp[i])) {
                    curr.push_back(p_inp[i]);
                } else {
                    if (p_inp[i] == '(') {
                        if (!curr.empty()) {
                            queue.push(curr);
                        }
                        queue.emplace("(");
                        curr = "";
                    } else if (p_inp[i] == ')') {
                        if (queue.empty()) throw out_of_range("Wrong bracket placement");
                        while (queue.top()[0] != '(') {
                            res.append(queue.top());
                            res.push_back(' ');
                            queue.pop();
                        }
                        queue.pop();
                        if (isalpha(queue.top().back())) {
                            res.append(queue.top());
                            res.push_back(' ');
                            queue.pop();
                        }
                    } else {
                        while (!queue.empty() && (priority[queue.top()[0]] >= priority[p_inp[i]])) {
                            res.append(queue.top());
                            res.push_back(' ');
                            queue.pop();
                        }
                        string c;
                        c.push_back(p_inp[i]);
                        queue.push(c);
                    }
                }
            }
        }
    }
    if (!curr.empty()) {
        res.append(curr);
        res.push_back(' ');
    }
    while (!queue.empty()) {
        res.append(queue.top());
        res.push_back(' ');
        queue.pop();
    }
    return res;
}

double calc(string equation, double x = 0) { //Вычисление в обратной польской записи с подстановкой х
    stack<double> st;
    for (int i = 0; i < equation.length(); i++) {
        string operand;
        while (equation[i] != ' ') {
            operand.push_back(equation[i]);
            i++;
        }
        if (operand == "x") {
            st.push(x);
            operand = "";
        } else if (operand == "e") {
            st.push(M_E);
        } else if (operand == "pi") {
            st.push(M_PI);
        } else if (isdigit(operand.back())) {
            st.push(strtod(operand.c_str(), nullptr));
        } else {
            if (operand == "+") {
                double a = st.top();
                st.pop();
                double b = st.top();
                st.pop();
                st.push(a + b);
            } else if (operand == "-") {
                double a = st.top();
                st.pop();
                double b = st.top();
                st.pop();
                st.push(b - a);
            } else if (operand == "*") {
                double a = st.top();
                st.pop();
                double b = st.top();
                st.pop();
                st.push(b * a);
            } else if (operand == "/") {
                double a = st.top();
                st.pop();
                double b = st.top();
                st.pop();
                st.push(b / a);
            } else if (operand == "^") {
                double a = st.top();
                st.pop();
                double b = st.top();
                st.pop();
                st.push(pow(b, a));
            } else if (operand == "sin") {
                double a = st.top();
                st.pop();
                st.push(sin(a));
            } else if (operand == "cos") {
                double a = st.top();
                st.pop();
                st.push(cos(a));
            } else if (operand == "tg") {
                double a = st.top();
                st.pop();
                st.push(tan(a));
            } else if (operand == "ctg") {
                double a = st.top();
                st.pop();
                st.push(1 / tan(a));
            } else if (operand == "arcsin") {
                double a = st.top();
                st.pop();
                st.push(asin(a));
            } else if (operand == "arccos") {
                double a = st.top();
                st.pop();
                st.push(acos(a));
            } else if (operand == "arctg") {
                double a = st.top();
                st.pop();
                st.push(atan(a));
            } else if (operand == "arcctg") {
                double a = st.top();
                st.pop();
                st.push(atan(1 / a));
            } else if (operand == "sqrt") {
                double a = st.top();
                st.pop();
                st.push(sqrt(a));
            } else if (operand == "lg") {
                double a = st.top();
                st.pop();
                st.push(log10(a));
            } else if (operand == "ln") {
                double a = st.top();
                st.pop();
                st.push(log(a));
            } else if (operand == "abs") {
                double a = st.top();
                st.pop();
                st.push(abs(a));
            }
        }
    }
    return st.top();
}

double integrate(const string &f, double a, double b) { //Вычисление определенного интеграла методом трапеций
    double h = (b - a) / INTEGRATION_STEPS;
    double ans = (calc(f, a) + calc(f, b)) / 2;
    for (double i = a + h; i < b;) {
        ans += calc(f, i);
        i += h;
    }
    ans *= h;
    return ans;
}

string fourier(const string &f, double l, unsigned int n) { //Вычисление коэффициентов Фурье
    double a0 = integrate(f, -l, l) / l / 2;
    a0 = round(a0);
    string ans;
    if (a0 != 0) {
        ans = sanitize(to_string(a0));
        ans.push_back(' ');
    }
    for (int i = 1; i <= n; i++) {
        string fa = f + "pi x " + to_string(i) + " * * " + to_string(l) + " / cos * ";
        double an = integrate(fa, -l, l) / l;
        string fb = f + "pi x " + to_string(i) + " * * " + to_string(l) + " / sin * ";
        double bn = integrate(fb, -l, l) / l;
        an = round(an);
        bn = round(bn);
        double c = round(M_PI * i / l);
        if (!ans.empty()) {
            if (an > 0) {
                ans.append("+ " + ((abs(an - 1) > EPSILON) ? (sanitize(to_string(an)) + " * ") : "") + "cos(" +
                           ((abs(c - 1) > EPSILON) ? (
                                   sanitize(to_string(c)) + " * ") : "") + "x) ");
            } else if (an < 0) {
                ans.append("- " + ((abs(-an - 1) > EPSILON) ? (sanitize(to_string(-an)) + " * ") : "") + "cos(" +
                           ((abs(c - 1) > EPSILON) ? (
                                   sanitize(to_string(c)) + " * ") : "") + "x) ");
            }
        } else if (an != 0) {
            ans.append(((abs(an - 1) > EPSILON) ? (sanitize(to_string(an)) + " * ") : "") + "cos(" +
                       ((abs(c - 1) > EPSILON) ? (
                               sanitize(to_string(c)) + " * ") : "") + "x) ");
        }
        if (!ans.empty()) {
            if (bn > 0) {
                ans.append("+ " + ((abs(bn - 1) > EPSILON) ? (sanitize(to_string(bn)) + " * ") : "") + "sin(" +
                           ((abs(c - 1) > EPSILON) ? (
                                   sanitize(to_string(c)) + " * ") : "") + "x) ");
            } else if (bn < 0) {
                ans.append("- " + ((abs(-bn - 1) > EPSILON) ? (sanitize(to_string(-bn)) + " * ") : "") + "sin(" +
                           ((abs(c - 1) > EPSILON) ? (
                                   sanitize(to_string(c)) + " * ") : "") + "x) ");
            }
        } else if (bn != 0) {
            ans.append(((abs(bn - 1) > EPSILON) ? (sanitize(to_string(bn)) + " * ") : "") + "sin(" +
                       ((abs(c - 1) > EPSILON) ? (
                               sanitize(to_string(c)) + " * ") : "") + "x) ");
        }
    }
    return ans;
}

int main() {

    main_start:
    string f;
    unsigned int n;
    string l_inp;
    double l;
    cout << "Fourier Series for custom function f(x)" << endl;
    cout << "Accepted functions and symbols:" << endl << \
    "+, -, *, / - arithmetic operations" << endl << \
    "(, ) - brackets" << endl << \
    "pi, e - constants" << endl << \
    "sqrt() - square root" << endl << \
    "abs() - absolute value" << endl << \
    "sin(), cos(), tg(), ctg() - trig functions" << endl << \
    "arcsin(), arccos(), arctg(), arcctg() - inverse trig functions" << endl << \
    "ln() - natural log" << endl << \
    "log() - log base 10" << endl << \
    "All other symbols are ignored." << endl << endl << \
    "The function should be continuous and integrable in the desired interval!" << endl << endl;

    input_label:
    cout << "f(x) = ";
    try {
        f = input();
    } catch (exception &e) {
        cerr << "Exception while parsing input:" << endl << e.what() << endl;
        goto input_label;
    }

    half_period_label:
    cout << "Half-period l = ";
    cin >> l_inp;
    if (l_inp == "pi" || l_inp == "PI" || l_inp == "Pi" || l_inp == "pI") {
        l = M_PI;
    } else if (l_inp == "e" || l_inp == "E") {
        l = M_E;
    } else {
        l = strtod(l_inp.c_str(), nullptr);
        if (l == INFINITY || l == NAN || l <= 0) {
            cerr << "Wrong input" << endl;
            goto half_period_label;
        }
    }

    number_input_label:
    cout << "Number of terms n = ";
    cin >> n;
    if (n <= 0) goto number_input_label;
    try {
        cout << "f(x) ~ " << fourier(f, l, n) << endl;
    } catch (exception &e) {
        cerr << "Exception during calculations:" << endl << e.what() << endl;
        goto main_start;
    }
    system("pause");
    return 0;
}
