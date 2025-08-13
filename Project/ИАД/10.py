import random
import numpy as np

# Функция активации (сигмоида)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Функция для one-hot кодирования (для просчитывания ошибки)
def one_hot_encode(label, num_classes=10):
    return np.eye(num_classes)[label]

# Функция прямого прохода сигнала через сеть
def forward_propagation(data, W, B):
    activations = [data]
    for i in range(len(W)):
        z = np.dot(activations[i], W[i].T) + B[i] # Вычисление линейного преобразования(взвешенная сумма входных данных)
        a = sigmoid(z)
        activations.append(a)
    return activations

# Функция для добавления шума к данным
def add_noise(pattern, noise_level=0.1):
    noisy_pattern = pattern.copy()
    num_elements = len(noisy_pattern)
    num_to_change = int(num_elements * noise_level)

    indices_to_change = random.sample(range(num_elements), num_to_change)

    for index in indices_to_change:
        noisy_pattern[index] = 1 - noisy_pattern[index]

    return noisy_pattern

# Функция обучения ИНС (обновление весов и смещений)
def train_AI(labeled_data, W, B, mu=0.1, noise_level=0.1, num_classes=10):
    # Подготовка начальных данных
    X_noisy = [add_noise(pattern, noise_level) for pattern in [ld[0] for ld in labeled_data]]
    X = np.array(X_noisy, dtype=np.float32)
    y = np.array([ld[1] for ld in labeled_data], dtype=np.int32)
    y_onehot = np.array([one_hot_encode(label, num_classes) for label in y], dtype=np.float32)

    # Определяются выходы из слоёв(прямое распространение)
    activations = forward_propagation(X, W, B)
    output = activations[-1]

    # Обратное распространение ошибки
    errors = [None] * len(W)
    errors[-1] = (y_onehot - output) * output * (1 - output)
    for i in reversed(range(len(W) - 1)):
        errors[i] = errors[i + 1].dot(W[i + 1]) * activations[i + 1] * (1 - activations[i + 1])

    # Обновление весов и смещений

    for i in range(len(W)):
        W[i] += errors[i].T.dot(activations[i]) * mu
        B[i] += np.sum(errors[i], axis=0) * mu

    return W, B

# Создание начальных весов и смещений
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

# итоговый вывод Нейронной сети
def predict(test_data, W, B):
    activations = forward_propagation(np.array([td[0] for td in test_data], dtype=np.float32), W, B)
    outputs = activations[-1]
    predictions = np.argmax(outputs, axis=1)
    real = np.array([td[1] for td in test_data])
    errors = np.sum(predictions != real)
    return errors, predictions, real


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

digits_10x10 = [
    [0,0,0,0,1,1,1,0,0,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,0,0,1,1,1,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,
     0,0,1,1,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,1,1,0,0,0,
     0,0,1,1,1,1,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,1,1,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,1,1,0,0,0,0,0,
     0,0,1,1,1,1,1,1,0,0,
     0,0,1,1,1,1,1,1,1,0],
    [0,0,0,1,1,1,1,0,0,0,
     0,0,1,1,0,1,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,1,1,1,1,0,0,0,
     0,0,0,1,1,1,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,1,0,
     0,0,0,0,0,0,1,1,0,0,
     0,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,1,1,1,0,0,
     0,0,0,0,1,1,1,1,0,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,0,1,0,0,1,1,0,0,
     0,0,1,1,0,0,1,1,0,0,
     0,0,1,1,1,1,1,1,1,0,
     0,0,1,1,1,1,1,1,1,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0],
    [0,0,1,1,1,1,1,0,0,0,
     0,0,1,1,1,1,1,0,0,0,
     0,0,1,0,0,0,0,0,0,0,
     0,0,1,0,0,0,0,0,0,0,
     0,0,1,1,1,1,0,0,0,0,
     0,0,0,0,1,1,1,0,0,0,
     0,0,0,0,0,1,1,1,0,0,
     0,0,0,0,0,1,1,1,0,0,
     0,0,0,0,1,1,1,0,0,0,
     0,0,1,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,1,0,0,
     0,0,0,1,1,1,1,1,0,0,
     0,0,1,1,0,0,0,0,0,0,
     0,0,1,1,0,0,0,0,0,0,
     0,0,1,1,1,1,1,1,0,0,
     0,0,1,1,1,0,1,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,1,0,1,1,1,0,
     0,0,0,1,1,1,1,1,0,0],
    [0,0,1,1,1,1,1,1,0,0,
     0,0,1,1,1,1,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,1,1,0,0,0,
     0,0,0,0,0,1,0,0,0,0,
     0,0,0,0,1,1,0,0,0,0,
     0,0,0,1,1,0,0,0,0,0,
     0,0,0,1,1,0,0,0,0,0,
     0,0,1,1,1,0,0,0,0,0,
     0,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,0,0,1,1,1,0,0,0,
     0,0,0,0,1,1,1,0,0,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,0,1,1,0,1,1,0,0,
     0,0,0,0,1,1,1,0,0,0,],
    [0,0,0,1,1,1,1,1,0,0,
     0,0,1,1,1,0,1,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,0,0,0,1,1,0,
     0,0,1,1,1,0,1,1,1,0,
     0,0,1,1,1,1,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,0,0,0,1,1,0,0,
     0,0,0,1,1,1,1,1,0,0,
     0,0,0,1,1,1,1,0,0,0,]
]


# 5х5
# Преобразование данных к нужному виду
X = [np.array(digit, dtype=np.float32) for digit in digits_5x5]
y = labels

# Создание весов и смещений и начальных данных
W, B = rand_params(25, [20, 10])
labeled_data = list(zip(X, y))

print("Тренировка:")
# тренировка и тестирование ИНС
for i in range(301):
    W, B = train_AI(labeled_data, W, B, mu=0.1, noise_level=0.0)

    if i % 50 == 0:
        errors, predictions, actual = predict(labeled_data, W, B)
        print(f"Эпоха: {i} \nТренировочные ошибки: {errors / len(labeled_data)}, {errors} из {len(labeled_data)}\nПредсказание: {predictions}\nРеальные данные: {actual}")

test_data_noisy = [add_noise(pattern, noise_level=0.1) for pattern in X]
test_set = list(zip(test_data_noisy, y))
test_error, predictions, actual = predict(test_set, W, B)
print(f"Тест:\nТестовые ошибки: {test_error / len(labeled_data)}, {test_error} из {len(labeled_data)}\nПредсказание: {predictions}\nРеальные данные: {actual}")

# 10x10
X_10x10 = [np.array(digit, dtype=np.float32) for digit in digits_10x10]
y_10x10 = labels
print(len(X_10x10[0]))
# Создание весов и смещений и начальных данных
W_10x10, B_10x10 = rand_params(100, [20, 20, 10])
labeled_data_10x10 = list(zip(X_10x10, y_10x10))
# Тренировка и тестирование ИНС
print("Тренировка 10х10:")
for i in range(501):
    W_10x10, B_10x10 = train_AI(labeled_data_10x10, W_10x10, B_10x10, mu=0.1, noise_level=0.0)

    if i % 100 == 0:
        errors_10x10, predictions_10x10, actual_10x10 = predict(labeled_data_10x10, W_10x10, B_10x10)
        print(f"Эпоха: {i}\nТренировочные ошибки: {errors_10x10 / len(labeled_data_10x10)}, {errors_10x10} из {len(labeled_data_10x10)}")

test_data_noisy_10x10 = [add_noise(pattern, noise_level=0.05) for pattern in X_10x10]
test_set_10x10 = list(zip(test_data_noisy_10x10, y_10x10))
test_error_10x10, predictions_10x10, actual_10x10 = predict(test_set_10x10, W_10x10, B_10x10)
print("Тестовая 10х10:")
print(f"Тестовая ошибка: {test_error_10x10 / len(test_set_10x10)}, {test_error_10x10} / {len(test_set_10x10)}")
print(f"Предсказанные: {predictions_10x10}")
print(f"Реальные:      {actual_10x10}")