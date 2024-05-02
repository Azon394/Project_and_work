import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def f(x):
    return x

def fourier_coefficients(n, f):
    a_coeffs = np.zeros(n)
    b_coeffs = np.zeros(n)
    a0, _ = quad(f, -np.pi, np.pi)
    a0 /= np.pi
    for i in range(1, n):
        a_coeffs[i], _ = quad(lambda x: f(x) * np.cos(i * x), -np.pi, np.pi)
        b_coeffs[i], _ = quad(lambda x: f(x) * np.sin(i * x), -np.pi, np.pi)
        a_coeffs[i] /= np.pi
        b_coeffs[i] /= np.pi
    return a0, a_coeffs, b_coeffs

def fourier_series(x, a0, a_coeffs, b_coeffs):
    n = len(a_coeffs)
    series_sum = a0 / 2
    for i in range(1, n):
        series_sum += a_coeffs[i] * np.cos(i * x) + b_coeffs[i] * np.sin(i * x)
    return series_sum

def main(n=1):
    n += 4
    a0, a_coeffs, b_coeffs = fourier_coefficients(n, f)
    print("Коэффициенты ряда Фурье:")
    print(f"a0 = {a0:.2f}")
    for i, (a, b) in enumerate(zip(a_coeffs, b_coeffs), 1):
        print(f"a{i} = {a:.2f}, b{i} = {b:.2f}")
    x_values = np.linspace(-np.pi, np.pi, 1000)
    y_values = [fourier_series(x, a0, a_coeffs, b_coeffs) for x in x_values]
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, f(x_values), label='Исходная функция')
    plt.plot(x_values, y_values, label=f'Ряд Фурье (n={n})')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Разложение функции в ряд Фурье')
    plt.legend()
    plt.grid(True)
    plt.show()

main()
