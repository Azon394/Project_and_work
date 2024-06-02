package main

import (
	"fmt"
	"math/rand"
	"sort"
	"time"
)

// Представление особи
type Individual struct {
	Chromosome []int // Набор индексов выбранных предметов
	Fitness    int   // Приспособленность особи (суммарная стоимость предметов)
}

// Функция для создания случайной особи
func createIndividual(n int) Individual {
	individual := Individual{}
	individual.Chromosome = make([]int, n)
	for i := range individual.Chromosome {
		individual.Chromosome[i] = rand.Intn(2) // Случайно выбираем, берем предмет или нет (1 - берем, 0 - не берем)
	}
	return individual
}

// Функция для оценки приспособленности особи
func evaluate(individual Individual, weights []int, values []int, capacity int) int {
	totalWeight := 0
	totalValue := 0
	for i, gene := range individual.Chromosome {
		if gene == 1 {
			totalWeight += weights[i]
			totalValue += values[i]
		}
	}
	// Если вес не превышает вместимость, возвращаем стоимость предметов, иначе 0
	if totalWeight <= capacity {
		return totalValue
	}
	return 0
}

// Функция для сортировки особей по приспособленности
type ByFitness []Individual

func (a ByFitness) Len() int           { return len(a) }
func (a ByFitness) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByFitness) Less(i, j int) bool { return a[i].Fitness > a[j].Fitness }

// Функция для выбора особей для скрещивания (турнирный отбор)
func tournamentSelection(population []Individual, tournamentSize int) Individual {
	rand.Shuffle(len(population), func(i, j int) {
		population[i], population[j] = population[j], population[i]
	})
	tournament := population[:tournamentSize]
	sort.Sort(ByFitness(tournament))
	return tournament[0]
}

// Функция для скрещивания двух особей (одноточечный кроссовер)
func crossover(parent1 Individual, parent2 Individual) Individual {
	child := Individual{}
	child.Chromosome = make([]int, len(parent1.Chromosome))
	crossoverPoint := rand.Intn(len(parent1.Chromosome))
	for i := 0; i < crossoverPoint; i++ {
		child.Chromosome[i] = parent1.Chromosome[i]
	}
	for i := crossoverPoint; i < len(parent1.Chromosome); i++ {
		child.Chromosome[i] = parent2.Chromosome[i]
	}
	return child
}

// Функция для мутации особи (инвертирование случайного гена)
func mutate(individual Individual, mutationRate float64) Individual {
	for i := range individual.Chromosome {
		if rand.Float64() < mutationRate {
			individual.Chromosome[i] = 1 - individual.Chromosome[i] // Инвертирование гена
		}
	}
	return individual
}

// Главная функция генетического алгоритма
func geneticAlgorithm(weights []int, values []int, capacity int, populationSize int, mutationRate float64, generations int) Individual {
	rand.Seed(time.Now().UnixNano())

	// Создание начальной популяции
	var population []Individual
	for i := 0; i < populationSize; i++ {
		population = append(population, createIndividual(len(weights)))
	}

	// Основной цикл генетического алгоритма
	for generation := 0; generation < generations; generation++ {
		// Оценка приспособленности каждой особи в популяции
		for i := range population {
			population[i].Fitness = evaluate(population[i], weights, values, capacity)
		}

		// Выбор особей для скрещивания и скрещивание
		var newPopulation []Individual
		for i := 0; i < populationSize; i++ {
			parent1 := tournamentSelection(population, 5)
			parent2 := tournamentSelection(population, 5)
			child := crossover(parent1, parent2)
			newPopulation = append(newPopulation, child)
		}

		// Мутация новой популяции
		for i := range newPopulation {
			newPopulation[i] = mutate(newPopulation[i], mutationRate)
		}

		// Замена старой популяции новой
		population = newPopulation
	}

	// Оценка приспособленности каждой особи в конечной популяции
	for i := range population {
		population[i].Fitness = evaluate(population[i], weights, values, capacity)
	}

	// Выбор лучшей особи (особи с наибольшей приспособленностью)
	sort.Sort(ByFitness(population))
	return population[0]
}

func main() {
	weights := []int{10, 5, 2, 3}
	values := []int{20, 30, 10, 20}
	capacity := 15
	populationSize := 100
	mutationRate := 0.1
	generations := 100

	bestIndividual := geneticAlgorithm(weights, values, capacity, populationSize, mutationRate, generations)

	fmt.Println("Номера элементов, помещенных в рюкзак:", bestIndividual.Chromosome)
	fmt.Println("Максимальная стоимость, которую можно унести в рюкзаке:", bestIndividual.Fitness)
}
