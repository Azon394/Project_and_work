package main

import (
	"fmt"
	"math"

	"gonum.org/v1/gonum/integrate"
)

func sim(f func(float64) float64, a, b float64) float64 {
	x := make([]float64, 0)
	y := make([]float64, 0)
	for i := a; i < b; i += 0.01 {
		x = append(x, i)
		y = append(y, f(i))
	}
	x = append(x, b)
	y = append(y, f(b))
	return integrate.Simpsons(x, y)
}

func Furie(f func(float64) float64, l, N float64) []float64 {
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
	return cof
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

func main() {
	var l float64 = 1
	var N float64 = 3
	cof := Furie(func(x float64) float64 { return x }, l, N)
	fmt.Print(cof[0])
	for i := 1; i < len(cof); i++ {
		if cof[i] >= 0 {
			fmt.Print("+")
		}
		if i%2 == 0 {
			fmt.Print(cof[i], "*cos(", float64(i)*math.Pi/l, "x)")
		} else {
			fmt.Print(cof[i], "*sin(", float64(i)*math.Pi/l, "x)")
		}
	}
}
