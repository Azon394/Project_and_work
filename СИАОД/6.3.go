package main

import (
	"fmt"
	"math"
)

func f(x float64) float64 {
	return x*x + 5*x + 6
}

func df(x float64) float64 {
	return 2*x + 5
}

func ddf(x float64) float64 {
	return 2
}

func newtonMethod(initialGuess float64, tolerance float64, maxIterations int) float64 {
	x := initialGuess

	for i := 0; i < maxIterations; i++ {
		gradient := df(x)
		hessian := ddf(x)

		if math.Abs(gradient) < tolerance {
			break
		}

		x = x - gradient/hessian
	}

	return x
}

func main() {
	initialGuess := 0.0
	tolerance := 1e-4
	maxIterations := 1000

	minimum := newtonMethod(initialGuess, tolerance, maxIterations)
	fmt.Printf("Минимум функции: %f\n", minimum)
	fmt.Printf("Значение функции в минимуме: %f\n", f(minimum))
}
