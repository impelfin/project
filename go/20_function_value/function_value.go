package main

import (
    "fmt"
    "math"
)

func compute(fn func(float64, float64) float64) float64 {
    return fn(3, 4)
}

func main() {
    // ① 함수를 변수에 할당해, 변수를 함수처럼 씀
    hypot := func(x, y float64) float64 {
        return math.Sqrt(x*x + y*y)
    }
    fmt.Println("① 변수를 통해 함수 호출 : ", hypot(5, 12))
    
    // ② 함수를 compute 함수에 인자로 전달함
    fmt.Println("② 함수를 함수에 인자로 전달")
    fmt.Println("compute(hypot) :\t\t", compute(hypot))
    fmt.Println("compute(math.Pow) :\t", compute(math.Pow))
}
