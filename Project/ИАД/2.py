import numpy as np
import matplotlib.pyplot as plt
import time

# Параметры
k = 1  # Замените на ваш номер в журнале
dt = 2 * np.pi / 1000
L = k / 100
omega = 1000 / k
t = np.linspace(0, 2 * np.pi, 500)

# Инициализация ряда
x = np.zeros(500)
x[1] = (-1)**k * dt

# Генерация ряда
for i in range(2, 500):
    x[i] = x[i-1] * (2 + dt * L * (1 - x[i-2]**2)) - x[i-2] * (1 + dt**2 + dt * L * (1 - x[i-2]**2)) + dt**2 * np.sin(omega * t[i])

# Реализация функций
def gradient(f, params, epsilon=1e-8):
    grad = np.zeros_like(params)
    for i in range(len(params)):
        params_eps = np.copy(params)
        params_eps[i] += epsilon
        grad[i] = (f(params_eps) - f(params)) / epsilon
    return grad

def gradient_descent(f, gradient, start, learn_rate, n_iter):
    params = np.copy(start)
    for _ in range(n_iter):
        grad = gradient(f, params)
        params -= learn_rate * grad
    return params

def minimize_stochastic(f, gradient, start, learn_rate, n_iter):
    params = np.copy(start)
    for _ in range(n_iter):
        idx = np.random.randint(0, len(params))
        grad = gradient(f, params)
        params[idx] -= learn_rate * grad[idx]
    return params

# Функция для аппроксимации ряда
def f(params, t):
    a1, b1, a2, b2, omega = params
    return a1 * np.sin(omega * t) + b1 * np.cos(omega * t) + a2 * np.sin(2 * omega * t) + b2 * np.cos(2 * omega * t)

# Функция ошибки
def F(params):
    return np.sum((x - f(params, t))**2)

# Начальные параметры
initial_params = np.random.rand(5)

# Применение градиентного спуска
params_gd = gradient_descent(F, gradient, initial_params, learn_rate=0.01, n_iter=1000)
print("Параметры, найденные методом градиентного спуска:", params_gd)

# Применение стохастического градиентного спуска
params_sgd = minimize_stochastic(F, gradient, initial_params, learn_rate=0.01, n_iter=1000)
print("Параметры, найденные методом стохастического градиентного спуска:", params_sgd)

# Время работы градиентного спуска
start_time_gd = time.time()
params_gd = gradient_descent(F, gradient, initial_params, learn_rate=0.01, n_iter=1000)
end_time_gd = time.time()
print("Время работы градиентного спуска:", end_time_gd - start_time_gd)

# Время работы стохастического градиентного спуска
start_time_sgd = time.time()
params_sgd = minimize_stochastic(F, gradient, initial_params, learn_rate=0.01, n_iter=1000)
end_time_sgd = time.time()
print("Время работы стохастического градиентного спуска:", end_time_sgd - start_time_sgd)