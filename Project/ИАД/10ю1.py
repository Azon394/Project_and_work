
import random
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def add_noise(pattern, noise_level=0.1):
    noisy_pattern = pattern.copy()
    num_elements = len(noisy_pattern)
    num_to_change = int(num_elements * noise_level)

    indices_to_change = random.sample(range(num_elements), num_to_change)

    for index in indices_to_change:
        noisy_pattern[index] = 1 - noisy_pattern[index]

    return noisy_pattern
def forward_propagation(data, W, B):
    activations = [data]
    for i in range(len(W)):
        z = np.dot(activations[i], W[i].T) + B[i] # Вычисление линейного преобразования(взвешенная сумма входных данных)
        a = sigmoid(z)
        activations.append(a)
    return activations
def rand_params(entry, layers):
    W, B = [], []
    for i, layer_size in enumerate(layers): # Проход по слою и кол-ву нейронов в слое
        if i == 0:
            w = np.random.rand(layer_size, entry) - 0.5
        else:
            w = np.random.rand(layer_size, layers[i - 1]) - 0.5
        b = np.zeros(layer_size)
        W.append(w)
        B.append(b)
    return W, B

def train(labled_data, W, B, mu=0.1, noise_level=0.1,):

    X_noisy = [add_noise(pattern, noise_level) for pattern in [ld[0] for ld in labeled_data]]
    X = np.array(X_noisy, dtype=np.float32)
    y = np.array([ld[1] for ld in labeled_data], dtype=np.int32)

    activations = forward_propagation(X, W, B)
    output = activations[-1]

    errors = [None] * len(W)
    errors[-1] = (y - output) * output * (1 - output)
    for i in reversed(range(len(W) - 1)):
        errors[i] = errors[i + 1].dot(W[i + 1]) * activations[i + 1] * (1 - activations[i + 1])


digits_5x5 = [
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],  # 0
    [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0],  # 1
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1],  # 2
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],  # 3
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],  # 4
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],  # 5
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],  # 6
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],  # 7
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0],  # 8
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],  # 9
]
labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

X = [np.array(digit, dtype=np.float32) for digit in digits_5x5]
y = labels

# Создание весов и смещений и начальных данных
W, B = rand_params(25, [20, 10])
labeled_data = list(zip(X, y))
train(X,W,B)











