from dsmltf import knn_classify, principal_components
from genser import transform_to
import csv



data = []
with open("iris.csv", "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        values = [float(x) for x in row[:-1]]
        variety = row[-1]
        data.append((values,variety))



print("\nБез снижения размерности")
for k in range(19, 30):
    n_correct = 0
    for flower in data:
        values, variety = flower
        other_flowers = [other_flower for other_flower in data if other_flower != flower]
        predicted_br = knn_classify(k, other_flowers, values)
        if predicted_br == variety:
            n_correct +=1
    print(k, "соседей:",n_correct,"правильных из", len(data))


print("\nСнижение методом PCA")
z = [i[0] for i in data]
pca_values = principal_components(z, 2)
pca_variety = [i[1] for i in data]
pca_data = []
for i in range(len(pca_values)):
    pca_data.append((pca_values[i], pca_variety[i]))
for k in range(1,30):
    n_correct = 0
    for flower in pca_data:
        values, variety = flower
        other_flowers = [other_flower for other_flower in pca_data if other_flower != flower]
        predicted_br = knn_classify(k, other_flowers, values)
        if predicted_br == variety:
            n_correct +=1
    print(k, "соседей:",n_correct,"правильных из", len(pca_data))

print("\nСнижение методом обобщенной сериализации")
genser_values = transform_to(z, 2)[0]
genser_variety = [i[1] for i in data]
genser_data = []
for i in range(len(genser_values)):
    genser_data.append((genser_values[i], genser_variety[i]))
for k in range(1,30):
    n_correct = 0
    for flower in genser_data:
        values, variety = flower
        other_flowers = [other_flower for other_flower in genser_data if other_flower != flower]
        predicted_br = knn_classify(k, other_flowers, values)
        if predicted_br == variety:
            n_correct +=1
    print(k, "соседей:",n_correct,"правильных из", len(genser_data))

#