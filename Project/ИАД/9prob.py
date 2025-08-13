from dsmltf import squared_distance, scale, distance, KMeans
from collections import defaultdict
from math import sqrt
import random
import csv


def squared_errors(inps, k):
    clasterbuilder = KMeans(k)
    clasterbuilder.train(inps)
    means = clasterbuilder.means
    inclaster = map(clasterbuilder.classify, inps)
    return sum(squared_distance(inp, means[cluster])
               for inp, cluster in zip(inps, inclaster))

# culmen_length_mm,culmen_depth_mm,flipper_length_mm,body_mass_g,sex
def getdata():
    data = []
    with open("penguins.csv", "r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            row[0] = row[0].replace(u'\ufeff', '')
            data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
    return data

def getdata2():
    data = []
    with open("DiamondsPrices.csv", "r", encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            row[0] = row[0].replace(u'\ufeff', '')
            data.append([float(row[5]), float(row[4]), float(row[7])])
    return data

def unify(clstrs, i, j):
    # i<j
    newcl = clstrs[i]+clstrs[j]
    clstrs[i] = newcl
    del clstrs[j]
    for k in range(j+1, len(clstrs)+1):
        clstrs[k-1] = clstrs.pop(k)
    return clstrs

def euclidean_dist(x,y):
    return sum((xi-yi)**2 for xi,yi in zip(x,y))**(1/2)

def clcenter(C):
    return [sum(x[i] for x in C)/len(C) for i, _ in enumerate(C[0])]
def cldist(C1,C2,dist):
    return dist(clcenter(C1),clcenter(C2))

def risingclustering(data, dist,size):
    clusters = {}
    for i, d in enumerate(data):
        clusters[i] = [d]
    dt = 0
    while dt < size:
        n = len(clusters)
        distances = {}
        for i in range(n-1):
            for j in range(i+1,n):
                distances[str(i)+','+str(j)] = cldist(clusters[i],clusters[j],dist)
        #print(distances)
        sij, dt = sorted(distances.items(), key=lambda x: x[1])[0]
        ij = sij.split(',')
        clusters = unify(clusters, int(ij[0]), int(ij[1]))
    return clusters

data = [[1,2,3],[2,3,4],[3,4,5],[1,2,3],[2,3,4],[3,4,5],[1,2,3],[2,3,4],[3,4,5]]
data = scale(getdata())
#print(data)
prev = []
for k in range(1, 10):
    x = squared_errors(data, k)
    prev.append(x)
print(prev)
# clasters = KMeans(4)
# clasters.train(data)
# for p in clasters.means:
#     print(p)
#
# B = risingclustering(data, euclidean_dist, 2)
# for k, v in B.items():
#     print(k, v)


