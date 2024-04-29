package main

import (
	"fmt"
	"math"
)

type pointFunc func(float64) float64

func sim_integral(f pointFunc, a float64, b float64, n int) float64 {
	h := (b - a) / float64(n) // шаг
	var k1 float64 = 0        // переменные для сохранения значений функции в чётных и нечётных точках
	var k2 float64 = 0
	for i := 1; i < n-1; i += 2 { // высчитываем значения функции при чётных и нечётных точках исключая крайние точки
		k1 += f(a + float64(i)*h)
		if i+1 >= n-1 {
			break
		}
		k2 += f(a + float64(i+1)*h)
	}
	return h / 3 * (f(a) + 4*k1 + 2*k2 + f(b)) // считаем интеграл по формуле
}

func integ(f pointFunc, a float64, b float64) float64 {
	var s1 float64
	var s float64
	var eps float64 = 0.0001
	var runge float64
	n := 100
	s1 = sim_integral(f, a, b, n) // первое приближение для интеграла
	for {
		s = s1 // второе приближение
		n = 2 * n
		s1 = sim_integral(f, a, b, n) // считаем интеграл для нового кол-ва шагов
		runge = (s1 - s) / 15
		if math.Abs(runge) <= eps {
			break
		}
	}
	return s1
}

func sim(f func(float64) float64, a, b float64) float64 {
	return integ(f, a, b)
}

func Furie(f func(float64) float64, l, N float64, x []float64) []float64 {
	cof := make([]float64, 0)
	cof = append(cof, sim(f, -l, l)/l)
	for i := 1.0; i < N+1; i++ {
		an := func(x float64) float64 {
			return f(x) * math.Cos((math.Pi*i*x)/l)
		}
		bn := func(x float64) float64 {
			return f(x) * math.Sin((math.Pi*i*x)/l)
		}
		cof = append(cof, sim(an, -l, l)/l)
		cof = append(cof, sim(bn, -l, l)/l)
	}
	result := make([]float64, 0)
	for _, val := range x {
		res := cof[0] / 2
		for n := 1.0; n < N+1; n++ {
			res += cof[2*int(n)-1]*math.Cos((math.Pi*n*val)/l) + cof[2*int(n)]*math.Sin((math.Pi*n*val)/l)
		}
		result = append(result, res)
	}
	return result
}

func ComputeMAE(arr1, arr2 []float64) float64 {
	if len(arr1) != len(arr2) {
		panic("Arrays have different lengths")
	}

	var sumError float64
	for i := 0; i < len(arr1); i++ {
		sumError += math.Abs(arr1[i] - arr2[i])
	}

	return sumError / float64(len(arr1))
}

func f(x float64) float64 {
	return x - x*x
}

func main() {
	result := make([]float64, 0)
	x := make([]float64, 0)
	result = Furie(f, 2, 4, x)
	fmt.Println(result)
}
