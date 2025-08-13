from dsmltf import dot, scale, train_test_split, gradient_descent, negate
import random
from math import exp, log
from functools import partial
def sigmoid(x):
    return 1.0/(1+exp(-x))

def log_likelyhood_i(x_i,y_i,beta):
    if y_i == 1:
        return log(sigmoid(dot(x_i,beta)))
    else:
        return log(1 - sigmoid(dot(x_i,beta)))

def log_likelyhood(x,y,beta):
    return sum(log_likelyhood_i(x_i,y_i,beta) for x_i,y_i in zip(x,y))

x = []
y = []
for i in range(500): #                     ЦЕНА                            ПЛОЩАДЬ           КОЛ-ВО КОМНАТ              ЭТАЖ
    x.append([random.randint(100000, 50000000), random.randrange(10, 100), random.randint(1, 4), random.randint(1, 9)])
    if x[i][0]/x[i][1] > 1000000 or (x[i][0]>30000000 and (x[i][2] < 3 or x[i][3] > 7)) or x[i][1]/x[i][2] < 20:
        y.append(0)
    else: y.append(1)
print(x[:5], y[:5])
sc_x = scale(x) # шкалирование

random.seed(0)
x_train,x_test,y_train,y_test = train_test_split(sc_x,y,0.33) # разбиение на обучающую и тестовую выборки

fn = partial(log_likelyhood,x_train,y_train)

beta_0 = [random.random() for _ in range(4)] # Устанавливаем отправную точку

beta_hat = gradient_descent(negate(fn), beta_0)[0] # максимизируем fn градиентным спуском

true_positives, false_negatives, false_positives, true_negatives = 0,0,0,0 # проверка на тестовой выборке
for x_i,y_i in zip(x_test, y_test):
    predict = sigmoid(dot(beta_hat, x_i))
    if y_i == 1 and predict >= 0.5:
        true_positives +=1
    elif y_i == 1:
        false_negatives +=1
    elif predict >= 0.5:
        false_positives +=1
    else:
        true_negatives +=1

precision = true_positives/(true_positives+false_positives)
recall = true_positives/(true_positives+false_negatives)
print(precision, recall)
