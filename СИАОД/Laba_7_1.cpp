#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int dynpack(int W, vector<int>& wt, vector<int>& val,unsigned int n) {
    vector<vector<int>> K(n + 1, vector<int>(W + 1));
    for (int i = 1; i <= n; i++) {
        for (int w = 1; w <= W; w++) {
            if (i == 0 || w == 0)
                K[i][w] = 0;
            else if (wt[i - 1] <= w)
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
            else
                K[i][w] = K[i - 1][w];

            for (int w = 0; w <= W; w++) {
                cout << K[i][w] << " ";
            }
            cout << endl;
        }
    }
    return K[n][W];
}
int main(){
    int n, cost0, weight0;
    int W = 60; //предельное значение рюкзака
    vector<int> cost; //стоимость предметов
    vector<int> weight; //вес каждого предмета
    cout << "Enter n: ";
    cin >> n;
    for (int i = 0; i < n; i++) {
        cout << "Enter the cost and weight: ";
        cin >> cost0 >> weight0;
        cost.push_back(cost0);
        weight.push_back(weight0);
    }
    cout << dynpack(W, weight, cost, cost.size())<< "- max cost"  << endl;
}