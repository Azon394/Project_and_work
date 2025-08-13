import csv
from dsmltf import scale, KMeans, squared_errors, is_leaf, get_children, distance, squared_distance, generate_clusters
import matplotlib.pyplot as plt

def bottom_up_cluster(inps, distance_agg=min):
    clusters = [(inp,) for inp in inps]
    while len(clusters) > 1:
        c1, c2 = min([(cluster1, cluster2)
                      for i, cluster1 in enumerate(clusters)
                      for cluster2 in clusters[:i]],
                     key=lambda x: cluster_distance( *x, distance_agg))
        clusters = [c for c in clusters if c != c1 and c != c2]
        merged_cluster = (len(clusters), [c1, c2])
        clusters.append(merged_cluster)
    return clusters[0]

def squared_errors(inps, k):
    clasterbuilder = KMeans(k)
    clasterbuilder.train(inps)
    means = clasterbuilder.means
    inclaster = map(clasterbuilder.classify, inps)
    return sum(squared_distance(inp, means[cluster])
               for inp, cluster in zip(inps, inclaster))

def get_values(cluster):
    if is_leaf(cluster):
        return [cluster[0]]
    else:
        return [val for child in get_children(cluster) for val in get_values(child)]

def cluster_distance(cluster1, cluster2, distance_agg=min):
    values1 = list(get_values(cluster1))
    values2 = list(get_values(cluster2))
    return distance_agg([distance(list(inp1), list(inp2)) for inp1 in values1 for inp2 in values2])

def take_data():
    with open('DiamondsPrices.csv', "r+", encoding="UTF-8") as f:
        data = list()

        a = {
            "Fair": 0,
            "Good": 1,
            "Very Good": 2,
            "Ideal": 3,
            "Premium": 4
        }
        b = {
            "I1": 0,
            "IF": 1,
            "SI1": 2,
            "SI2": 3,
            "VS1": 4,
            "VS2": 5,
            "VVS1": 6,
            "VVS2": 7,
        }
        for line in csv.reader(f):
            data.append(line[1:3] + line[4:6])
        for i in range(1, len(data)):
            data[i][0] = a[data[i][0]]
            data[i][1] = b[data[i][1]]
            data[i][2] = float(data[i][2])
            data[i][3] = int(data[i][3])
        return data[1:]

def plt_k(scaled_data: list):
    x, y = list(), list()
    for k in range(1, 20):
        x.append(k)
        y.append(squared_errors(scaled_data, k))
        print(k)
    print(x)
    print(y)
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label='', marker='o')
    plt.show()


def main():
    # получение данных
    data = take_data()
    # шкалирование данных
    scaled_data = scale(data[:100])

    # Поиск нужного k (k = 20)
    #plt_k(scaled_data)
    #     x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    #     y = [215759.99999999092, 174055.41146246, 170098.27734130874, 170666.4118288543, 124835.31814370902, 144810.5082265626,
    #      117054.68743773685, 97474.54852205738, 89325.73781496486, 112415.9329158144, 87865.35685806836, 90250.02420816086,
    #      91210.12301518251, 109904.68025590049, 80321.2228246056, 81404.9151551547, 83534.33527402098, 65923.56862211417,
    #      67585.58623978352]

    # кластеризация k средних
    clasters = KMeans(8)
    clasters.train(scaled_data)
    print(clasters.means)

    # кластеризация восходящая
    base_claster = bottom_up_cluster(scaled_data)
    print([get_values(cluster) for cluster in generate_clusters(base_claster, 8)])

if __name__ == '__main__':
    main()