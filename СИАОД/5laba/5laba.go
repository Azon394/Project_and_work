package main

import (
	"fmt"
	"gonum.org/v1/gonum/integrate"
	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
	"math"
)

func f(x float64) float64 {
	return math.Abs(math.Sin(x))
}

func fourierCoefficients(n int, f func(float64) float64) (float64, []float64, []float64) {
	aCoeffs := make([]float64, n)
	bCoeffs := make([]float64, n)
	a0 := integrate.Simpsons(f, -math.Pi, math.Pi, 1000)
	a0 /= math.Pi
	for i := 1; i < n; i++ {
		aCoeffs[i] = integrate.Fixed(func(x float64) float64 { return f(x) * math.Cos(float64(i)*x) }, -math.Pi, math.Pi, 1000)
		bCoeffs[i] = integrate.Fixed(func(x float64) float64 { return f(x) * math.Sin(float64(i)*x) }, -math.Pi, math.Pi, 1000)
		aCoeffs[i] /= math.Pi
		bCoeffs[i] /= math.Pi
	}
	return a0, aCoeffs, bCoeffs
}

func fourierSeries(x float64, a0 float64, aCoeffs []float64, bCoeffs []float64) float64 {
	n := len(aCoeffs)
	seriesSum := a0 / 2
	for i := 1; i < n; i++ {
		seriesSum += aCoeffs[i]*math.Cos(float64(i)*x) + bCoeffs[i]*math.Sin(float64(i)*x)
	}
	return seriesSum
}

func main() {
	n := 3
	a0, aCoeffs, bCoeffs := fourierCoefficients(n, f)
	fmt.Println("Коэффициенты ряда Фурье:")
	fmt.Printf("a0 = %.2f\n", a0)
	for i, a := range aCoeffs[1:] {
		b := bCoeffs[i+1]
		fmt.Printf("a%d = %.2f, b%d = %.2f\n", i+1, a, i+1, b)
	}
	xValues := make([]float64, 1000)
	yValues := make([]float64, 1000)
	for i := 0; i < 1000; i++ {
		xValues[i] = -math.Pi + 2*math.Pi*float64(i)/999
		yValues[i] = fourierSeries(xValues[i], a0, aCoeffs, bCoeffs)
	}
	pts := make(plotter.XYs, len(xValues))
	for i := range pts {
		pts[i].X = xValues[i]
		pts[i].Y = yValues[i]
	}
	p, _ := plot.New()
	p.Title.Text = "Разложение функции в ряд Фурье"
	p.X.Label.Text = "x"
	p.Y.Label.Text = "y"
	l, _ := plotter.NewLine(pts)
	p.Add(l)
	p.Save(10*vg.Inch, 6*vg.Inch, "fourier.png")
}
