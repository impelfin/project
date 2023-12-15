package main

import "fmt"

func main() {
    // ① 배열선언과 원소 초기화를 따로
    var a [2]string
    a[0] = "Hello"
    a[1] = "World"
    fmt.Println("a[0], a[1] :", a[0], a[1])
    fmt.Println("a :", a)
    
    // ② 배열선언과 초기화를 동시에
    primes := [6]int{2, 3, 5, 7, 11, 13}
    fmt.Println("primes :", primes)
}
